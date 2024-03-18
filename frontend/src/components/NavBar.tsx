import React from 'react';
import { SignInButton, SignOutButton } from "@clerk/clerk-react";
import {useUser} from "@clerk/clerk-react";
import {
  Box,
  Flex,
  Text,
  Button,
  useColorModeValue,
} from '@chakra-ui/react';
import { useConvexAuth } from 'convex/react';

const NavBar: React.FC = () => {
  const { isAuthenticated } = useConvexAuth();
  const {user} = useUser();
  return (
    <Box bg={useColorModeValue('white', 'gray.800')} px={4} py={3} borderBottom="1px" borderColor="gray.200">
      <Flex alignItems="center" justifyContent="space-between">
        <Text fontSize="xx-large" fontWeight="bold" color={useColorModeValue('gray.800', 'white')}>
          FinanQ
        </Text>

        {/* Sign In and Sign Up buttons */}
        <Flex>
          {!isAuthenticated ? (
            <Button colorScheme='pink'>
              <SignInButton mode="modal" />
            </Button>
          ) : (
            <Flex alignItems="center">
              <Text fontSize="md">{user?.fullName}</Text>
              <Button ml={2} colorScheme='red'>
                <SignOutButton />
              </Button>
            </Flex>
          )}
        </Flex>
      </Flex>
    </Box>
  );
};

export default NavBar;
