// convex/functions.ts
import dotenv from 'dotenv';
dotenv.config();
import { action } from "./_generated/server";
import { v } from "convex/values";

// Define a Convex action function to send text to Flask API
export const sendTextToFlask = action({
  
  args: { text: v.string() }, // Define an argument 'text' of type string
  handler: async (_, args) => { // Define a handler function that receives arguments
    try {
      const response = await fetch(process.env.SERVER_URL+'/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: args.text }), // Send input text to Flask API
      });
      
      const data = await response.json(); // Parse response JSON
      return data.answer; // Return response from Flask API
    } catch (error) {
      console.error("Error sending text to Backend:", error);
      throw error; // Propagate error if encountered
    }
  },
});
