import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { ClerkProvider, useAuth } from "@clerk/clerk-react";
import { ConvexProviderWithClerk } from "convex/react-clerk";
import { ConvexReactClient } from "convex/react";
import { ChakraProvider } from "@chakra-ui/react";


const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL as string);

ReactDOM.render(
  <React.StrictMode>
    <ChakraProvider> {/* Pass your Chakra UI theme */}
      <ClerkProvider publishableKey="pk_test_aW1tb3J0YWwtcG9sZWNhdC02MS5jbGVyay5hY2NvdW50cy5kZXYk">
        <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
          <App />
        </ConvexProviderWithClerk>
      </ClerkProvider>
    </ChakraProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

