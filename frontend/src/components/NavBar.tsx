import React from 'react';
import { Link } from 'react-router-dom';
import { SignInButton } from "@clerk/clerk-react";
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
          <Button colorScheme='pink'>
            <SignInButton mode="modal" />
            {/* Sign In */}
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
};

export default NavBar;
