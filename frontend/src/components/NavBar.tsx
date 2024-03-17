import React from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Flex,
  Text,
  Button,
  useColorModeValue,
} from '@chakra-ui/react';

const NavBar: React.FC = () => {
  return (
    <Box bg={useColorModeValue('white', 'gray.800')} px={4} py={3} borderBottom="1px" borderColor="gray.200">
      <Flex alignItems="center" justifyContent="space-between">
        <Text fontSize="xl" fontWeight="bold" color={useColorModeValue('gray.800', 'white')}>
          Your Logo
        </Text> 

        {/* Sign In and Sign Up buttons */}
        <Flex>
          <Button variant="ghost" as={Link} to="/signin" mr={2}>
            Sign In
          </Button>
          <Button as={Link} to="/signup" colorScheme="pink">
            Sign Up
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
};

export default NavBar;
