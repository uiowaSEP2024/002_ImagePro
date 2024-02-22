import React from "react";
import { Flex, Box, Icon, Text } from "@chakra-ui/react";
import { MdErrorOutline } from "react-icons/md/index.js";

interface ErrorMessageBoxProps {
  errorMessage: string;
}

const ErrorMessageBox: React.FC<ErrorMessageBoxProps> = ({ errorMessage }) => {
  return (
    <Flex alignItems="center">
      <Box
        bgColor="white"
        borderColor="red.500"
        borderWidth="2px"
        marginBlock={"25px"}
        p={4}
        borderRadius="md"
        display="flex"
        alignItems="center"
      >
        <Icon as={MdErrorOutline} color="red.500" boxSize={6} />
        <Text color="red.500" ml={2}>
          {errorMessage}
        </Text>
      </Box>
    </Flex>
  );
};

export default ErrorMessageBox;
