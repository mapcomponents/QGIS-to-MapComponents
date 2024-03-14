import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";

type Props = {
  selectedFeature?: GeoJSON.Feature;
};

const FeatureInfoProps = (props: Props) => {
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {props.selectedFeature &&
        Object.keys(props.selectedFeature?.properties).map((key) => (
          <>
            <ListItem key={key}>
              <ListItemText
                primary={props.selectedFeature.properties[key]}
                secondary={key}
              />
            </ListItem>
            <br />
          </>
        ))}
    </List>
  );
};

export default FeatureInfoProps;
