import React, { Dispatch, SetStateAction, useEffect, useState } from "react";

const MapComponentizerContext = React.createContext({});
const MapComponentizerProvider = MapComponentizerContext.Provider;

const MapComponentizerContextProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [layers, setLayers] = useState<any[]>([]);
  const [config, setConfig] = useState<any>();

  console.log(layers);
  console.log(config)


  const fetchLayerFiles = async (
    setter: Dispatch<SetStateAction<any[]>>,
    orderList: string[]
  ) => {
    const filesPromises = orderList.reverse().map(async (layer) => {
      try {
        const fileResponse = await fetch(`../exported/${layer}.json`);
        const fileData = await fileResponse.json();
        return fileData;
      } catch (error) {
        console.error(`Error fetching ${layer}.json:`, error);
        //catch error; // Rethrow the error to make Promise.all catch it
        return null;
      }
    });
  
    try {
      // Filter out layers that were not fetched successfully (null values)
      const fetchedLayers = (await Promise.all(filesPromises)).filter(layer => layer !== null);
      setter(fetchedLayers);
    } catch (error) {
      console.error("Error fetching layers:", error);
    }
  };

useEffect(()=>{
  config?.order && fetchLayerFiles(setLayers, config.order)

}, [config])
 
  
  //get layer lists for each layer type
  useEffect(() => {
    // Call the fetchData function when the component mounts
    const fetchConfig = async (setter: Dispatch<SetStateAction<string[]>>) => {
      const configResponse = await fetch(`../exported/config.json`);
      const config = await configResponse.json();
      setter(config);
    };

    fetchConfig(setConfig);
  }, []);

  const stateProviderValue = {
    layers,
    config
  };

  return (
    <MapComponentizerProvider value={stateProviderValue}>
      {children}
    </MapComponentizerProvider>
  );
};

export { MapComponentizerContext, MapComponentizerContextProvider };