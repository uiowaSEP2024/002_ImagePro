import React from "react";
import { Flex, Box, Icon, Text } from "@chakra-ui/react";
import { MdErrorOutline } from "react-icons/md/index.js";

/**
 * ErrorMessageBoxProps is a type that represents the properties of the ErrorMessageBox component.
 * It includes the error message to be displayed.
 */
interface ErrorMessageBoxProps {
  errorMessage: string;
}

/**
 * ErrorMessageBox is a functional component that renders an error message box.
 * The error message box includes an error icon and the error message.
 *
 * @param {object} props - The properties passed to the component.
 * @param {string} props.errorMessage - The error message to be displayed.
 * @returns {JSX.Element} The ErrorMessageBox component.
 */
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
