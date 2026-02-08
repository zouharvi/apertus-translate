// typst compile scripts/04b-render_metrics.typ outputs/04b-render_metrics.pdf --root .

#import "@preview/booktabs:0.0.4": *
#show: booktabs-default-table-style
#set page(height: auto, width: auto, margin: 2em)
#set text(font: "TeX Gyre Termes")

#let metrics = json("../outputs/04-metrics.json")

#let format_cell(model, x) = {
  let (min, max) = (0.6, 0.7)
  let color = white.mix(
    (green, calc.max((x - min) / (max - min), 0) * 500%),
    (red, calc.max((max - x) / (max - min), 0) * 500%),
  )

  let s = str(calc.round(x, digits: 3))
  if not s.contains(".") { s += "." }
  let tail = s.split(".").last()
  (
    table.cell(fill: color, box(width: 3cm, model)),
    table.cell(fill: color, s + "0" * (3 - tail.len())),
  )
}

#set align(top)

#{
  stack(
    dir: ltr,
    spacing: 2em,
    ..metrics
      .pairs()
      .map(((dataset, models_scores)) => {
        (
          dataset
            + table(
              columns: 2,
              ..models_scores
                .pairs()
                .map(
                  ((model, score)) => format_cell(model, score),
                )
                .flatten()
            )
        )
      }),
  )
}
