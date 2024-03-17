import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { ConvexProvider, ConvexReactClient } from "convex/react";
import { ChakraProvider } from "@chakra-ui/react";


const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL as string);

ReactDOM.render(
  <React.StrictMode>
    <ChakraProvider> {/* Pass your Chakra UI theme */}
      <ConvexProvider client={convex}>
        <App />
      </ConvexProvider>
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
