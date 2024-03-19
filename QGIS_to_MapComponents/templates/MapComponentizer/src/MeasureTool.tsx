import { MlMeasureTool } from "@mapcomponents/react-maplibre";
import React from "react";

import { Divider, Box, Typography } from "@mui/material";

const MeasureTool = () => {
  return (
    <>
      <Box>
        <Divider sx={{ marginBottom: "20px" }} />
        <Typography variant={"h6"}>Measure Line</Typography>
        <Box m={2} style={{ textAlign: "left" }}>
          <MlMeasureTool measureType="line" unit="kilometers" />
        </Box>
      </Box>
    </>
  );
};

export default MeasureTool;
