/**
 * This file contains the Reporting component of the application.
 * The Reporting component is a React component that provides a feature for the user to download a report of all studies that have been completed by their provider.
 * It fetches the user's input for the start and end dates, validates it, and attempts to fetch the report.
 */

// Import necessary libraries, components, hooks, and types.
import {
  Badge,
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  HStack,
  Heading,
  Input,
  Text,
  VStack
} from "@chakra-ui/react";
import { withAuthenticated } from "@/components/withAuthenticated";
import { useState } from "react";
import { fetchDownloadReport } from "@/data";

/**
 * The Reporting component is a React component that provides a feature for the user to download a report of all studies that have been completed by their provider.
 * It fetches the user's input for the start and end dates, validates it, and attempts to fetch the report.
 */
function Reporting() {
  // Initialize the start and end dates for the report.
  const initialEndDate = new Date();
  const initialStartDate = new Date(initialEndDate);
  initialStartDate.setFullYear(initialStartDate.getFullYear() - 1);

  // Initialize state variables for the start and end dates.
  const [reportStartDate, setReportStartDate] = useState<string>(
    initialStartDate.toISOString().split("T")[0]
  );
  const [reportEndDate, setReportEndDate] = useState<string>(
    initialEndDate.toISOString().split("T")[0]
  );

  // Render the Reporting component.
  return (
    <Container pt={8} maxW={"container.lg"} justifyContent={"center"}>
      <VStack align={"flex-start"} gap={2}>
        <Badge fontSize={"xl"} lineHeight={1.5} textAlign={"center"}>
          Reporting
        </Badge>

        <Box>
          <Heading size={"lg"}>Download Historical Studies</Heading>
          <Text>
            Download a CSV of all studies that have been completed by your provider
          </Text>

          <VStack align={"flex-start"}>
            <HStack>
              <FormControl>
                <FormLabel>Start Date</FormLabel>
                <Input
                  value={reportStartDate}
                  onChange={(e) => {
                    setReportStartDate(e.target.value);
                  }}
                  type={"date"}
                />
              </FormControl>

              <FormControl>
                <FormLabel>End Date</FormLabel>
                <Input
                  value={reportEndDate}
                  onChange={(e) => {
                    setReportEndDate(e.target.value);
                  }}
                  type={"date"}
                />
              </FormControl>
            </HStack>
            <Button
              onClick={() => {
                fetchDownloadReport(reportStartDate, reportEndDate);
              }}
            >
              Download
            </Button>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
}

/**
 * Export the Reporting component wrapped with the withAuthenticated higher-order component.
 */
export default withAuthenticated(Reporting, ["provider"]);
