// pages/Home.tsx
import React from 'react';
import NavBar from '../components/NavBar';
import { Box } from '@chakra-ui/react';
import DisplayCard from '../components/DisplayCard';

const Home: React.FC = () => {
  return (
    <Box>
      <NavBar />
      <Box mt={8} mx="auto" maxW="400px"> {/* Adjust styling as needed */}
        <DisplayCard />
      </Box>
    </Box>
  );
};

export default Home;
