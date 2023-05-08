import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";
import {
  Container,
  SimpleGrid,
  Image,
  Flex,
  Heading,
  Text,
  Stack,
  StackDivider,
  Icon,
  Box,
  Card,
  Link,
  CardHeader
} from "@chakra-ui/react";
import {
  IoAnalyticsSharp,
  IoLogoBitcoin,
  IoSearchSharp
} from "react-icons/io5";
import { ReactElement } from "react";
import NextLink from "next/link";

interface FeatureProps {
  text: string;
  iconBg: string;
  icon?: ReactElement;
  description?: string;
  link: string;
}
const Feature = ({ text, icon, iconBg, description, link }: FeatureProps) => {
  return (
    <Card>
      <Box p={3}>
        <Stack direction={"row"} align={"center"}>
          <Flex
            w={8}
            h={8}
            align={"center"}
            justify={"center"}
            rounded={"full"}
            bg={iconBg}
          >
            {icon}
          </Flex>
          <Text fontWeight={600}>{text}</Text>
        </Stack>
      </Box>
      <CardHeader>
        <Link
          as={NextLink}
          css={{ display: "block", width: "100%" }}
          href={link}
        >
          {description}
        </Link>
      </CardHeader>
    </Card>
  );
};

function Dashboard() {
  const { currentUser } = useAuthContext();

  const features = [
    {
      text: "Jobs",
      icon: <Icon as={IoSearchSharp} color={"purple.500"} w={5} h={5} />,
      iconBg: "purple.100",
      show: true,
      link: "/jobs",
      description: "View past and currently active jobs"
    },
    {
      text: "Analytics",
      icon: <Icon as={IoLogoBitcoin} color={"green.500"} w={5} h={5} />,
      iconBg: "green.100",
      show: currentUser?.role === "provider",
      link: "/analytics",
      description: "View analytics and data aggregation"
    },
    {
      text: "API Integration",
      icon: <Icon as={IoAnalyticsSharp} color={"yellow.500"} w={5} h={5} />,
      iconBg: "yellow.100",
      show: currentUser?.role === "provider",
      link: "/apikeys",
      description: "Generate API keys for your provider account"
    }
  ];

  return (
    <Container maxW={"5xl"} py={12}>
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={10}>
        <Stack spacing={4}>
          <Text
            textTransform={"uppercase"}
            color={"blue.400"}
            fontWeight={600}
            fontSize={"sm"}
            bg={"blue.50"}
            p={2}
            alignSelf={"flex-start"}
            rounded={"md"}
          >
            Dashboard
          </Text>
          <Heading>Explore our tools</Heading>
          <Text color={"gray"} fontSize={"lg"}>
            Your home base for all business operations you may need help with!
            From here, access all client jobs, individual progress, analytics,
            and more. Generate API keys to introduce our software to your
            existing workflow! With BotImage, we hope you find tracking progress
            on jobs easier than ever. Our motto: never let a client slip through
            the cracks.
          </Text>
          <Stack
            spacing={4}
            divider={<StackDivider borderColor={"gray.100"} />}
          >
            {features.map((feature, index) => {
              if (feature.show === false) {
                return null;
              }
              return (
                <Feature
                  key={index}
                  icon={feature.icon}
                  iconBg={feature.iconBg}
                  text={feature.text}
                  description={feature.description}
                  link={feature.link}
                />
              );
            })}
          </Stack>
        </Stack>
        <Flex pl={10}>
          <Image
            rounded={"md"}
            alt={"Artistic Representation of Tracking"}
            src={"/assets/dashboardart.png"}
            objectFit={"cover"}
          />
        </Flex>
      </SimpleGrid>
    </Container>
  );
}

export default withAuthenticated(Dashboard);
