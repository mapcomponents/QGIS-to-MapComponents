import React, { useEffect, useState } from "react";

const MapComponentizerContext = React.createContext({});
const MapComponentizerProvider = MapComponentizerContext.Provider;

const MapComponentizerContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [geojsonLayers, setGeojsonLayers] = useState<any[]>([]);
  const [geojsonIndex, setGeojsonIndex] = useState([]);
  const [wmsLayers, setWmsLayers] = useState();
console.log(geojsonLayers)
  useEffect(() => {
    const fetchGeojsonFiles = async () => {
      const filesPromises = geojsonIndex.map(async (layer) => {
        const fileResponse = await fetch(`../exported/geojson/${layer}`);
        const fileData = await fileResponse.json();
        return fileData;
      });
  
      try {
        const fetchedGeojsonLayers = await Promise.all(filesPromises);
        setGeojsonLayers(fetchedGeojsonLayers);
      } catch (error) {
        console.error('Error fetching GeoJSON files:', error);
      }
    };
  
    if (geojsonIndex.length > 0) {
      fetchGeojsonFiles();
    }
  }, [geojsonIndex]);


  useEffect(() => {
    const fetchData = async () => {
      // Fetch the index file
      const indexResponse = await fetch("../exported/geojson/index.json");
      const indexData = await indexResponse.json();

      setGeojsonIndex(indexData);
    };
    // Call the fetchData function when the component mounts
    fetchData();
  }, []);



  const stateProviderValue = {
    geojsonLayers,
    wmsLayers,
  };

  return (
    <MapComponentizerProvider value={stateProviderValue}>
      {children}
    </MapComponentizerProvider>
  );
};

export { MapComponentizerContext, MapComponentizerContextProvider };
