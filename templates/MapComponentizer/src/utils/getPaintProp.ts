const mapColors = [
    "#586A23",
    "#80842D",
    "#9C8C38",
    "#B48A43",
    "#CC824F",
    "#D57E65",
    "#DD7E7B",
    "#E4929E",
    "#EBA9BF",
    "#F2C1DA",
    "#F7D9EF"
    ];

export function getPaintProp(layerType: string, index: number) {

    const i = index % 9;

  switch (layerType) {
    case "fill":
      return {
        "fill-color": mapColors[i],
        "fill-outline-color": "#000",
        "fill-opacity": 0.9,
      };
    case "line": 
      return {
        "line-color": mapColors[i],
        "line-width": 2
      };
    case "circle": 
     return {
        "circle-radius": 4,
        "circle-color":  mapColors[i],
        "circle-stroke-color":  "#000"
     }  
    default:
      undefined

  }
}
