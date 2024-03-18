import React, { useState } from 'react';
import { Box, Button, Container, Heading, Input, Stack, Text } from '@chakra-ui/react';
import { useAction, useConvexAuth } from 'convex/react';
import { api } from '../../convex/_generated/api';
import { SignInButton } from "@clerk/clerk-react";

const DisplayCard: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [outputValue, setOutputValue] = useState('');
  const [loading, setLoading] = useState(false); // Add loading state
  const { isAuthenticated } = useConvexAuth();

  const sendTextToFlask = useAction(api.myFunctions.sendTextToFlask);

  const handleSubmit = async () => {
    setLoading(true); // Set loading to true when submitting
    try {
      const response = await sendTextToFlask({ text: inputValue });
      setOutputValue(response);
    } catch (error) {
      console.error('Error sending text to Flask API:', error);
    } finally {
      setLoading(false); // Set loading to false after API call completes
    }
  };

  return (
    <Container maxW="4xl">
      <Stack
        as={Box}
        textAlign="center"
        spacing={{ base: 8, md: 14 }}
        py={{ base: 20, md: 36 }}
      >
        <Heading
          fontWeight={600}
          fontSize={{ base: 'xl', sm: '2xl', md: '4xl' }}
          lineHeight="120%"
        >
          Know the info <br />
          <Text as="span" color="green.400">
            maximize your profits
          </Text>
          <br />
          <Text as="span" color="gray.500">
            Search your query
          </Text>
        </Heading>
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Enter something..."
          mb={4}
          style={{ width: '100%' }} 
        />
        <Button
          colorScheme="green"
          bg="green.400"
          rounded="full"
          px={6}
          onClick={isAuthenticated?handleSubmit: () =>{
            alert("Please sign in to continue.")
          }}
          _hover={{
            bg: 'green.500',
          }}
          isLoading={loading} // Set isLoading prop to loading state
          loadingText="Loading" // Optional loading text
        >
          Submit
        </Button>
        {outputValue && (
          <Box mt={4}>
            <Text fontWeight="bold">Output:</Text>
            <Text>{outputValue}</Text>
          </Box>
        )}
      </Stack>
    </Container>
  );
};

export default DisplayCard;
