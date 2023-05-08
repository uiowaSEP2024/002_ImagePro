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

function Reporting() {
  const initialEndDate = new Date();
  const initialStartDate = new Date(initialEndDate);
  initialStartDate.setFullYear(initialStartDate.getFullYear() - 1);

  const [reportStartDate, setReportStartDate] = useState<string>(
    initialStartDate.toISOString().split("T")[0]
  );
  const [reportEndDate, setReportEndDate] = useState<string>(
    initialEndDate.toISOString().split("T")[0]
  );

  return (
    <Container pt={8} maxW={"container.lg"} justifyContent={"center"}>
      <VStack align={"flex-start"} gap={2}>
        <Badge fontSize={"xl"} lineHeight={1.5} textAlign={"center"}>
          Reporting
        </Badge>

        <Box>
          <Heading size={"lg"}>Download Historical Jobs</Heading>
          <Text>
            Download a CSV of all jobs that have been completed by your provider
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

export default withAuthenticated(Reporting, ["provider"]);
