import { MlGeoJsonLayer, useMap } from "@mapcomponents/react-maplibre";
import React, { useEffect, useState } from "react";
import { PointLike, MapEventType } from "maplibre-gl";

type Props = {
  layers: string[];
};

function MlFeatureInfo(props: Props) {
  const mapHook = useMap();
  const [selectedFeature, setSelectedFeature] = useState();

  useEffect(() => {
    if (!mapHook.map) return;

    const mapClickHandler = (e: MapEventType) => {
      if (!mapHook.map) return;

      const availableLayers = mapHook.map.style._order;
      const clickLayers = props.layers.filter(
        (el) => availableLayers.indexOf(el) !== -1
      );

      console.log(clickLayers);
      console.log(props.layers);

      const bbox = [
        [e.point.x - 10, e.point.y - 10],
        [e.point.x + 10, e.point.y + 10],
      ];

      const f = mapHook.map.queryRenderedFeatures(
        bbox as [PointLike, PointLike],
        {
          layers: clickLayers,
        }
      );

      let infoFeature = undefined;
      f.forEach((el) => {
        if (
          el.layer.type === "line" &&
          (!infoFeature ||
            infoFeature?.layer?.type === "fill" ||
            infoFeature?.layer?.type === "circle")
        ) {
          infoFeature = el;
        }
        if (
          el.layer.type === "circle" &&
          (!infoFeature || infoFeature?.layer?.type === "fill")
        ) {
          infoFeature = el;
        }
        if (el.layer.type === "fill" && !infoFeature) {
          infoFeature = el;
        }
      });
      if (infoFeature) {
        let feature_id = infoFeature.id;

        console.log(infoFeature);
        setSelectedFeature(infoFeature.toJSON());
      }
    };

    mapHook.map.on("click", mapClickHandler);
    return () => {
      if (!mapHook.map) return;
      mapHook.map.off("click", mapClickHandler);
    };
  }, [props.layers, mapHook]);

  return (
    <div>
      <h2>MlFeatureInfo</h2>
      <p>
        {selectedFeature &&
          Object.keys(selectedFeature?.properties).map((key) => (
            <>
              {key}: {selectedFeature.properties[key]}
              <br />
            </>
          ))}
      </p>
      {selectedFeature && <MlGeoJsonLayer geojson={selectedFeature} />}
    </div>
  );
}

export default MlFeatureInfo;
