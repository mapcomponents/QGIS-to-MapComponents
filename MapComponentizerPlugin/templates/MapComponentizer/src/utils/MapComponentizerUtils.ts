import { useContext } from "react";
import { MapComponentizerContext } from "../MapComponentizerContext";
import {Feature, Polygon, Properties, bbox, bboxPolygon, centroid, featureCollection } from '@turf/turf';
import { LngLatBoundsLike } from 'maplibre-gl';

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
  "#F7D9EF",
];

export function getPaintProp(layer: any, index: number) {
  const getDefaultPaint = () => {
    const i = index % 9;

    switch (layer.geomType) {
      case "fill":
        return {
          "fill-color": mapColors[i],
          "fill-outline-color": "#000",
          "fill-opacity": 0.9,
        };
      case "line":
        return {
          "line-color": mapColors[i],
          "line-width": 2,
        };
      case "circle":
        return {
          "circle-radius": 4,
          "circle-color": mapColors[i],
          "circle-stroke-color": "#000",
        };
      default:
        undefined;
    }
  };

  const getExportedPaint = () => {
    switch (layer.geomType) {
      case "fill":

        const fill = layer.paint.layers?.filter((l) => l.type === "fill");
        const stroke = layer.paint.layers?.filter((l) => l.type === "line");

        return { 
          "fill-outline-color": stroke?.[0].paint?.["line-color"],
          ...fill?.[0].paint,         
        };

      case "line":

      const line = layer.paint.layers?.filter((l)=> l.type === "line");
        
        return {
          ...line?.[0]?.paint
        };

      case "circle":
        const circle =  layer.paint.layers?.filter((l) => l.type === "circle");

       return {
        ...circle?.[0].paint
       }
      default:
        return undefined;
    }
  };
 
  return layer.paint ? getExportedPaint() : getDefaultPaint();
}

export const getLabels = (layer: any)=>{
  const symbolConfig = layer.paint?.layers?.filter((l)=> l.type === "symbol")[0]
  const options = {"paint": symbolConfig?.paint, "layout": symbolConfig?.layout}
  if (options.layout && options.layout["text-font"]) {
    delete options.layout["text-font"];
  }
    return symbolConfig ? options  : {}  
  }


export const getprojectExtent: (layers: any)=>{"bbox": LngLatBoundsLike, "center": any} = (layers: any)=>{

  var polygons: Feature<Polygon, Properties>[] = []
  layers.filter((l)=> l.type === "geojson").forEach(layer => {

   polygons.push(bboxPolygon(bbox(layer.geojson)))

  });
  const extent ={"bbox": bbox(featureCollection(polygons)) as LngLatBoundsLike, "center": centroid(featureCollection(polygons))}
  
 
  return extent
}