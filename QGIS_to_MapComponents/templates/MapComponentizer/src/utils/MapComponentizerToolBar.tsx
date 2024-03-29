import { MlCreatePdfButton, TopToolbar } from "@mapcomponents/react-maplibre";
import { Button } from "@mui/material";
import LayersIcon from '@mui/icons-material/Layers';

export interface MapComponentizerToolBarProps {
  tools?: { icon: any; action: () => void }[];
}

export default function MapComponentizerToolBar(
  props: MapComponentizerToolBarProps
) {

  return (
    <>
      <TopToolbar unmovableButtons={<>
        
        {props.tools &&
          props.tools.map((tool) => (
            <Button variant="contained" onClick={tool.action} sx={{marginRight: 1}}>
             {tool.icon}
            </Button>
          ))}
          <MlCreatePdfButton />
      </>} />
    </>
  );
}
