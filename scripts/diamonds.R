## =====================================================================
## PICK UP HERE (NWH, 2026-07-31)
##
## 1. DONE. The old GAP put clearance of GAP/2 - RH before the node and GAP/2
##    after it, so the right side was ~6x wider. PAD replaces it: the literal
##    clearance either side of a node, applied symmetrically. Raise or lower
##    PAD alone. Saving goes through save_fit(), which derives height from the
##    plot's aspect, so recovered width becomes height instead of letterbox.
##
## 2. Loop lines and loop labels in the individual figures need work.
##    The loop drops from the node at -RH to -H-0.9, curves back to the
##    diamond midpoint, and the label sits at -H-1.22. The curvature=-.1 arc
##    and the label centring are the rough parts. The recombine arc in D3
##    (curvature=-.5, above the diamond) is separate and also needs a pass.
##
## 3. Tip sharpness is one parameter: TIP. Currently .52 in the strip and
##    .58 in the detail. Lower is closer to a true point; the tip labels
##    ("Domain", "People") are what will break first.
##
## Not yet done: Fira Sans registration; band widths are uniform rather than
## proportional to the effort each stage takes.
## =====================================================================

library(ggplot2); library(dplyr); library(svglite)

brand <- list(primary="#0A659E", gold="#E3A008", ink="#1F2937", muted="#9CA3AF")
MUTE_FILL <- "#E9EDF0"; MUTE_INK <- "#AEB6BD"; MUTE_GOLD <- "#DCDFE3"

## Brand typography. Set once as a geom default so every text layer inherits it,
## including annotate("text"), which is GeomText under the hood.
FONT <- "Fira Sans"
if (FONT %in% systemfonts::system_fonts()$family) {
  update_geom_defaults("text",  list(family = FONT))
  update_geom_defaults("label", list(family = FONT))
} else {
  message("note: ", FONT, " not installed - falling back to the default sans")
}
## Two-segment ramp. Diverge stays light enough for ink; converge dark enough
## for white. The step between them IS the diverge->converge transition marker.
DIV_RAMP <- c("#D8E9F4", "#93BFDB")
CON_RAMP <- c("#2878A8", "#0A5480")
PHASE_GAP <- 0.03                       # zero: the ramp step alone marks the transition

bands <- function(div, con, x0, SW, H, TIP) {
  n <- length(div); m <- length(con); Wd <- n*SW; Wc <- m*SW
  fd <- colorRampPalette(DIV_RAMP)(n); fc <- colorRampPalette(CON_RAMP)(m)
  hd <- function(x) TIP + (H-TIP)*(x-x0)/Wd
  xc0 <- x0 + Wd + PHASE_GAP
  hc <- function(x) TIP + (H-TIP)*(xc0+Wc-x)/Wc
  capL <- TIP*Wd/(H-TIP); capR <- TIP*Wc/(H-TIP)
  d <- do.call(rbind, lapply(1:n, function(i){
    x1 <- x0+(i-1)*SW; x2 <- x0+i*SW
    ## slice 1 absorbs the left cap: one triangle, no false seam at the join
    px <- if (i==1) c(x0-capL, x2, x2)      else c(x1,x2,x2,x1)
    py <- if (i==1) c(0, -hd(x2), hd(x2))   else c(-hd(x1),-hd(x2),hd(x2),hd(x1))
    data.frame(id=paste0("d",x0,i), x=px, y=py,
               lab=div[i], mid=(x1+x2)/2, fill=fd[i], col=brand$ink, outcome=FALSE,
               phase="diverge")}))
  cc <- do.call(rbind, lapply(1:m, function(i){
    x1 <- xc0+(i-1)*SW; x2 <- xc0+i*SW
    ## the outcome slice absorbs the right cap, so the gold keyline wraps the
    ## whole point instead of stopping at a seam short of it
    px <- if (i==m) c(x1, xc0+Wc+capR, x1)  else c(x1,x2,x2,x1)
    py <- if (i==m) c(-hc(x1), 0, hc(x1))   else c(-hc(x1),-hc(x2),hc(x2),hc(x1))
    data.frame(id=paste0("c",x0,i), x=px, y=py,
               lab=con[i], mid=(x1+x2)/2, fill=fc[i], col="white", outcome=(i==m),
               phase="converge")}))
  ## The point is now part of the end slice, so TIP no longer sets sharpness -
  ## it sets where the LABELLED band ends and the blank nose begins.
  list(poly=rbind(d,cc), right=xc0+Wc+capR, left=x0-capL,
       mid=x0+Wd+PHASE_GAP/2, capR=capR, run=Wc+capR,
       ## underside of the FIRST converge slice: a real edge for the loop-back to
       ## touch, rather than empty space below the shape. It sits lower than the
       ## slices to its right, so the arrow reaches it without crossing them.
       c1x=xc0+SW*.55, c1y=-hc(xc0+SW*.55),
       ## midpoints and edge heights per slice, so an arc can anchor to a NAMED
       ## slice and to the silhouette instead of floating on magic offsets
       dmid=x0+(seq_len(n)-.5)*SW, dtop=hd(x0+(seq_len(n)-.5)*SW),
       cmid=xc0+(seq_len(m)-.5)*SW, ctop=hc(xc0+(seq_len(m)-.5)*SW))
}

## node_style: "rhombus" (flowchart convention: a decision happens here) or
## "arrow"  (a forward arrow carrying the test name: shows motion and keeps the
## pass/fail asymmetry, since failure branches off the axis rather than mirroring
## it). A double-headed arrow was rejected: <-> conventionally reads as a
## bidirectional RELATIONSHIP, not a branch, and would claim a symmetry the
## process does not have.
build <- function(spec, SW=.62, H=3.1, TIP=.52, PAD=.22, RH=.92,
                  lab=2.5, node=2.3, tag=2.4, title=0, loop=TRUE, sub=FALSE,
                  handoff=FALSE, node_style=c("arrow","rhombus"),
                  focus=c("all","diverge","converge","test")) {
  node_style <- match.arg(node_style); focus <- match.arg(focus)
  ## Arrow geometry, scaled off RH so both styles read at the same weight.
  ## Sized to the label it carries, not to match the rhombus's footprint.
  ## ANT is the tail notch: a concave left edge that mirrors the head, so the
  ## shape reads as RECEIVING as well as sending. Without it the arrow looks
  ## already committed to going forward and the failure branch reads as an
  ## afterthought hanging off it.
  AL <- RH*1.02; AHL <- RH*0.52; ABH <- RH*0.58; AHH <- RH*0.92
  ## ANT is derived, not chosen: the notch is cut at the SAME angle as the
  ## diamond's converge edge (run/rise), so the join reads as one more step
  ## separator - a sideways V - rather than a foreign shape meeting the point.
  ANT <- ABH * (length(spec[[1]]$con)*SW + TIP*(length(spec[[1]]$con)*SW)/(H-TIP)) / H
  ## does this figure draw the recombine arc? decided up front, because the
  ## DIVERGE/CONVERGE label has to sit above it rather than be crossed by it
  has_rec <- any(vapply(spec, function(s) isTRUE(s$recomb), logical(1)))
  rec_up  <- focus=="converge" && has_rec
  rec_div <- focus=="diverge"  && has_rec
  P <- NULL; L <- NULL; N <- NULL; A <- NULL; x <- 0
  for (k in seq_along(spec)) {
    s <- spec[[k]]; b <- bands(s$div, s$con, x, SW, H, TIP)
    P <- rbind(P, b$poly)
    L <- rbind(L, b$poly %>% filter(!is.na(lab)) %>% group_by(lab) %>%
                 summarise(mid=first(mid), col=first(col), outcome=first(outcome), .groups="drop"))
    half <- if (node_style=="rhombus") RH else AL
    ## Arrow mode: seat the diamond's point INSIDE the tail notch, so the two
    ## shapes interlock instead of facing each other across a gap.
    tx <- if (node_style=="rhombus") b$right + PAD + half
          else b$right + .05 - ANT + AL
    nv <- if (node_style=="rhombus")
      data.frame(x=c(tx-RH,tx,tx+RH,tx), y=c(0,RH,0,-RH))
    else            # notched tail -> body -> head, one closed polygon
      data.frame(
        x=c(tx-AL,     tx+AL-AHL, tx+AL-AHL, tx+AL, tx+AL-AHL, tx+AL-AHL, tx-AL, tx-AL+ANT),
        y=c(-ABH,      -ABH,      -AHH,      0,     AHH,       ABH,       ABH,   0))
    N <- rbind(N, data.frame(dia=k, tx=tx, lab=s$test, nv))
    rf <- if (is.null(s$recomb_from)) 3L else s$recomb_from
    rt <- if (is.null(s$recomb_to))   4L else s$recomb_to
    A <- rbind(A, data.frame(dia=k, x0=b$right, tx=tx, xl=x, xm=b$mid, lab=s$test,
                             c1x=b$c1x, c1y=b$c1y,
                             rfx=b$cmid[rf], rfy=b$ctop[rf],
                             rtx=b$dmid[rt], rty=b$dtop[rt],
                             back=s$back, sub=s$sub, title=s$title,
                             recomb=isTRUE(s$recomb),
                             nL=tx-half, nR=tx+half,
                             ntx=if (node_style=="rhombus") tx else tx+(ANT-AHL)/2,
                             nbot=if (node_style=="rhombus") -RH else -ABH,
                             last=(k==length(spec))))
    x <- tx + half + PAD             # same clearance on the way out
  }
  ## Highlight by muting, never by cropping: the reader keeps the whole cycle in
  ## view and sees where in it this chapter sits. Cropping would throw away the
  ## "where am I" that the colour is there to answer.
  if (focus != "all") {
    off <- P$phase != focus
    P$fill[off] <- MUTE_FILL
    L$col[L$lab %in% P$lab[off]] <- MUTE_INK
    if (focus == "test") { P$fill[] <- MUTE_FILL; L$col[] <- MUTE_INK }
  }
  gold_now  <- if (focus %in% c("all","converge","test")) brand$gold else MUTE_GOLD
  node_now  <- if (focus %in% c("all","test")) brand$gold else MUTE_GOLD
  node_ink  <- if (focus %in% c("all","test")) "#4A3000" else MUTE_INK
  g <- ggplot() +
    geom_polygon(data=P, aes(x,y,group=id, fill=I(fill)), colour="white", linewidth=.55) +
    # outcome slice: gold keyline, rhyming with the gold node it feeds
    geom_polygon(data=P %>% filter(outcome), aes(x,y,group=id),
                 fill=NA, colour=gold_now, linewidth=.9) +
    geom_text(data=L, aes(mid, 0, label=lab), angle=90, size=lab,
              lineheight=.88, colour=L$col, fontface=ifelse(L$outcome,2,1))
  PHL <- if (rec_up || rec_div) 1.02 else .26   # phase label clears either arc
  for (i in seq_len(nrow(A))) {
    a <- A[i,]
    ## In arrow mode the notch receives the diamond's point, so the little
    ## in/out arrows are redundant and were removed.
    if (node_style=="rhombus") g <- g +
      annotate("segment", x=a$x0+.05, xend=a$nL-.06, y=0, yend=0,
               colour=brand$muted, linewidth=.55,
               arrow=arrow(length=unit(.11,"cm"), type="closed"))
    g <- g +
      ## Anchor the SEPARATOR on the phase boundary, not the string's centre.
      ## This dot genuinely encodes the diverge->converge transition, so it sits
      ## exactly on it. Three elements, not two: the dot must be its own centred
      ## mark. Bundling it into the left string with hjust=1 puts the dot's right
      ## EDGE on the boundary, which reads as off-centre. Offset scales with the
      ## type size so it holds at both the strip and detail scales.
      annotate("text", x=a$xm - tag*.075, y=H+PHL, label="DIVERGE", hjust=1,
               size=tag, fontface=2, colour=brand$muted) +
      annotate("text", x=a$xm, y=H+PHL, label="·", hjust=.5,
               size=tag, fontface=2, colour=brand$muted) +
      annotate("text", x=a$xm + tag*.075, y=H+PHL, label="CONVERGE", hjust=0,
               size=tag, fontface=2, colour=brand$muted)
    if (!a$last && node_style=="rhombus") g <- g +
      annotate("segment", x=a$nR+.06, xend=a$nR+PAD-.05, y=0, yend=0,
               colour=brand$primary, linewidth=.55,
               arrow=arrow(length=unit(.11,"cm"), type="closed"))
    if (loop) g <- g +
      annotate("curve", x=a$tx, xend=a$c1x, y=a$nbot-.06, yend=a$c1y-.10,
               curvature=-.42, angle=105, ncp=14,
               colour=brand$gold, linewidth=.6,
               arrow=arrow(length=unit(.13,"cm"), type="closed")) +
      ## sit just under the arc's belly, biased toward the node end where the
      ## arc is steepest - the label belongs to the return path, not to the
      ## empty space beneath the diamond
      annotate("text", x=a$tx*.58 + a$c1x*.42, y=a$c1y-.62, label=a$back,
               size=tag-.35, fontface=3, colour="#8A6100")
    ## D3's inner loop: recombine the best losers. It happens AT the screening
    ## matrix, so it appears ONLY on the convergence figure - the chapter that
    ## teaches it. On the whole-diamond figure it competed with the validation
    ## loop and read as a stray arc.
    ## NOT gated on `loop`: the validation loop and the recombine loop are
    ## different things. Convergence figures show this one with loop=FALSE.
    if (a$recomb && focus == "converge") g <- g +
      ## rise from the screening matrix, cross above the peak, descend into the
      ## recombination slice. One curve cannot do this: the peak sits BETWEEN the
      ## two anchors, so any single arc cuts the silhouette.
      annotate("segment", x=a$rfx, xend=a$rfx, y=a$rfy+.06, yend=H+.40,
               colour=brand$gold, linewidth=.6) +
      annotate("curve", x=a$rfx, xend=a$rtx, y=H+.40, yend=H+.40,
               curvature=.14, ncp=14, colour=brand$gold, linewidth=.6) +
      annotate("segment", x=a$rtx, xend=a$rtx, y=H+.40, yend=a$rty+.10,
               colour=brand$gold, linewidth=.6,
               arrow=arrow(length=unit(.12,"cm"), type="closed")) +
      annotate("text", x=a$rfx+SW*.30, y=H*.55, hjust=0, size=tag-.3,
               fontface=3, colour="#8A6100",
               label="work the concepts into better ones")   # covers both laps: first-pass
               ## elaboration AND salvaging the best of the screened-out concepts
    ## the vertical list replaces the inline run-on when the test IS the subject
    ## First-lap recombination: work a concept, feed the result back into the
    ## pool, repeat. No screening required - this is why a team can reach ~100
    ## ideas in half an hour rather than grinding for days.
    if (rec_div && a$recomb) g <- g +
      annotate("curve", x=a$rtx, xend=a$rtx-SW, y=a$rty+.20, yend=a$rty-.55,
               curvature=.85, ncp=16, colour=brand$gold, linewidth=.6,
               arrow=arrow(length=unit(.12,"cm"), type="closed")) +
      annotate("text", x=a$rtx+SW*.28, y=H*.60, hjust=0, size=tag-.3,
               fontface=3, colour="#8A6100",
               label="each pass feeds the pool again")
    if (sub && focus != "test" && nzchar(a$sub)) g <- g +
      annotate("text", x=a$tx, y=a$nbot-.62, label=a$sub, size=tag-.5, colour=brand$muted, fontface=3)
    ## Left-aligned at the diamond's left tip, deliberately NOT centred. Its
    ## separator divides an index from a name and encodes nothing structural,
    ## so it must not land near the phase gutter — a near-miss reads as a failed
    ## alignment and invites a meaning that isn't there. Off the axis entirely.
    if (title>0) g <- g +
      annotate("text", x=a$xl, y=if (loop) -H-1.42 else -H-.44, hjust=0,
               label=a$title, size=title, fontface=2, colour=brand$primary)
  }
  ## headroom must account for the recombine arc too, not just the loop below:
  ## the convergence figure draws that arc with loop = FALSE, and without this
  ## it was silently clipped by the panel.
  rec_up <- focus=="converge" && any(vapply(spec, function(s) isTRUE(s$recomb), logical(1)))
  xr <- c(-.3-TIP*2, x + if (handoff) 1.9 else if (focus=="test") 3.4 else .35)
  yr <- c(if (loop) -H-1.75 else -H-.72,
          H + if (loop) 1.75 else if (rec_up || rec_div) 1.45 else .58)
  g <- g + geom_polygon(data=N, aes(x,y,group=dia), fill=node_now, colour="white", linewidth=.7) +
    geom_text(data=A, aes(ntx, 0, label=lab), size=node,
              fontface=2, colour=node_ink, lineheight=.88) +
    (if (focus=="test" && nzchar(spec[[1]]$sub)) {
       tl <- trimws(strsplit(spec[[1]]$sub, "·", fixed=TRUE)[[1]])
       ty <- seq_along(tl); ty <- (mean(ty)-ty) * (tag*.115)
       list(annotate("text", x=A$nR[1]+PAD*2.2, y=ty, label=tl, hjust=0,
                     size=tag-.25, colour=brand$ink),
            annotate("text", x=A$nR[1]+PAD*2.2, y=max(ty)+tag*.16,
                     label="tests available", hjust=0, size=tag-.5,
                     fontface=3, colour=brand$muted))
     } else NULL) +
    (if (handoff) list(
      annotate("segment", x=x-PAD+.05, xend=x+1.5, y=0, yend=0, colour=brand$primary,
               linewidth=.6, arrow=arrow(length=unit(.13,"cm"), type="closed")),
      annotate("text", x=x+.78, y=.34, size=tag-.3, fontface=3, colour=brand$primary,
               label="profit analytics"),
      annotate("text", x=x+.78, y=-.34, size=tag-.45, fontface=3, colour=brand$muted,
               label="→ Is This Worth Doing?")) else NULL) +
    coord_fixed(xlim=xr, ylim=yr, expand=FALSE) +
    theme_void(base_family=FONT) + theme(plot.margin=margin(2,2,2,2))
  ## coord_fixed() locks the data aspect at 1:1. If ggsave's width/height does
  ## not match diff(xr)/diff(yr), ggplot letterboxes the panel and you get dead
  ## margin you cannot remove with GAP. Carry the aspect so ggsave can match it.
  attr(g, "aspect") <- diff(xr) / diff(yr)
  g
}

## Save at a canvas matching the plot's own aspect, so coord_fixed() never
## letterboxes. SVG, not PNG: these are line art displayed at ~25% width in the
## chapters, so vector stays crisp at any zoom, weighs less, and keeps the
## labels as REAL TEXT - searchable, selectable, and readable by a screen
## reader. The outlined-path SVGs this replaces had none of that.
save_fit <- function(path, g, width) {
  ggsave(path, g, width = width, height = width / attr(g, "aspect"), bg = "white")
  invisible(attr(g, "aspect"))
}

D1 <- list(div=c("Domain","Generate communities","Profile the people","Map their orbit"),
           con=c("Identify patterns","Growing empathy","Assess access","People"),
           test="Access\ntest", title="DIAMOND 1 · PEOPLE", sub="",
           back="not yet — converge on another community")
D2 <- list(div=c("Observe","Listen","Role play","Secondary research"),
           con=c("Cluster around themes","Develop personas","Map experiences","Pain"),
           test="Pain\nvalidation", title="DIAMOND 2 · PAIN",
           sub="pain validation · ouch factor · willingness to pay",
           back="not yet — abduce another pain from the same evidence")
D3 <- list(div=c("Fill the\ncatalog","Generate","Recombine"), recomb_to=3L,
           con=c("Feasibility filter","Dot voting","Screening matrix","Solution"),
           test="Solution\nvalidation", title="DIAMOND 3 · SOLUTION", recomb=TRUE,
           sub="customer validation · verification · wow factor · $100 · smoke test",
           back="not yet — return to the screened concepts")

## Output directory: the OUT env var if set, otherwise the working directory.
## (Previously OUT was required; unset it resolved to "" and ragg tried to write
## to the filesystem root -> "agg could not write to the given file".)

## Default output is the book's images/ directory, resolved relative to this
## script, so `Rscript scripts/diamonds.R` from the repo root just works.
O <- Sys.getenv("OUT")
if (!nzchar(O)) {
  args <- commandArgs(trailingOnly = FALSE)
  here <- dirname(sub("^--file=", "", args[grep("^--file=", args)]))
  O <- if (length(here)) normalizePath(file.path(here, "..", "images")) else getwd()
}
if (!dir.exists(O)) dir.create(O, recursive = TRUE)
## =====================================================================
## MANIFEST — every figure the book needs, from one source of truth.
## Change a label, the palette, or the geometry once; regenerate all of them.
## Flags: loop (show the "no" path) · handoff (point on to profit analytics)
##        focus (all|diverge|converge|test) · sub (name the tests)
## =====================================================================
DS <- list(D1, D2, D3)
DETAIL <- function(...) build(..., SW=.92, H=3.3, TIP=.58, PAD=.26, RH=1.05,
                              lab=3.4, node=3.1, tag=3.1, title=3.2)

## A · the spine: all three, low detail, no loops, ends in the handoff
## The node is a forward ARROW, not a rhombus. A rhombus shows the failure
## branch dropping away but says nothing about the pass; the arrow carries the
## forward motion in its shape, so the pair reads as "you will most likely go
## on, and occasionally loop back" - the asymmetry entrepreneurs actually face.
save_fit(file.path(O,"spine.svg"),
         build(DS, loop=FALSE, title=2.7, handoff=TRUE), width=13.8)

## C · one figure per diamond, with its loop-back. Only Diamond 3 hands off.
for (i in 1:3)
  save_fit(file.path(O, sprintf("diamond-%d.svg", i)),
           DETAIL(DS[i], loop=TRUE, handoff=(i==3)), width=9.6)

## B · one per chapter: the WHOLE diamond, other phases muted, so the reader
##     keeps the cycle in view and sees where this chapter sits inside it.
for (i in 1:3) for (ph in c("diverge","converge","test"))
  save_fit(file.path(O, sprintf("d%d-%s.svg", i, ph)),
           DETAIL(DS[i], loop=(ph=="test"), handoff=FALSE,
                  focus=ph, sub=(ph=="test")), width=9.6)

cat("  wrote 2 spine + 3 diamond + 9 chapter figures\n")
cat("ok\n")
