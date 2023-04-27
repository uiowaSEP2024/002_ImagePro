
import { useAuthContext } from "@/hooks/useAuthContext";
import { withAuthenticated } from "@/components/withAuthenticated";
import { Card, Link } from "@nextui-org/react";
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
  useColorModeValue,
} from '@chakra-ui/react';
import {
  IoAnalyticsSharp,
  IoLogoBitcoin,
  IoSearchSharp,
} from 'react-icons/io5';
import { ReactElement } from 'react';



function Dashboard() {
  const {currentUser} = useAuthContext()
  
  interface FeatureProps {
    text: string;
    iconBg: string;
    icon?: ReactElement;
  }
  
  const Feature = ({ text, icon, iconBg }: FeatureProps) => {
    return (
      <Stack direction={'row'} align={'center'}>
        <Flex
          w={8}
          h={8}
          align={'center'}
          justify={'center'}
          rounded={'full'}
          bg={iconBg}>
          {icon}
        </Flex>
        <Text fontWeight={600}>{text}</Text>
      </Stack>
    );
  };
  
  return (
      <Container maxW={'5xl'} py={12}>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={10}>
          <Stack spacing={4}>
            <Text
              textTransform={'uppercase'}
              color={'blue.400'}
              fontWeight={600}
              fontSize={'sm'}
              bg={useColorModeValue('blue.50', 'blue.900')}
              p={2}
              alignSelf={'flex-start'}
              rounded={'md'}>
              Dashboard
            </Text>
            <Heading>Explore our tools</Heading>
            <Text color={'gray.500'} fontSize={'lg'}>
              Your home base for all business operations you may need help with! From here, access all client jobs, individual progress,
              analytics, and more. Generate API keys to introduce our software to your existing workflow! With BotImage, we hope you find
              tracking progress on jobs easier than ever. Our motto: never let a client slip through the cracks.
            </Text>
            <Stack
              spacing={4}
              divider={
                <StackDivider
                  borderColor={useColorModeValue('gray.100', 'gray.700')}
                />
              }>
                <Card>
                  <Box p={3}>
                    <Feature
                    icon={
                      <Icon as={IoSearchSharp} color={'purple.500'} w={5} h={5} />
                    }
                    iconBg={useColorModeValue('purple.100', 'purple.900')}
                    text={'Jobs'} />
                  </Box>
                  <Card.Header>
                    <Link css={{ display: "block", width: "100%" }} href="/jobs">
                    View past and currently active jobs
                    </Link>
                  </Card.Header>
                </Card>
             
                            
                <Card>
                  <Box p={3}>
                    <Feature
                      icon={<Icon as={IoLogoBitcoin} color={'green.500'} w={5} h={5} />}
                      iconBg={useColorModeValue('green.100', 'green.900')}
                      text={'Analytics'} />
                  </Box>
                  <Card.Header>
                    <Link css={{ display: "block", width: "100%" }} href="/billing">
                      View analytics and data aggregation
                    </Link>
                  </Card.Header>
                </Card>

              <Card>
                <Box p={3}>
                  <Feature
                    icon={
                      <Icon as={IoAnalyticsSharp} color={'yellow.500'} w={5} h={5} />
                    }
                    iconBg={useColorModeValue('yellow.100', 'yellow.900')}
                    text={'API Integration'} />
                </Box>
                   <Card.Header>
                    <Link css={{ display: "block", width: "100%" }} href="/billing">
                      Generate API Keys to try out our system
                    </Link>
                  </Card.Header>
              </Card>

            </Stack>
          </Stack>
          <Flex pl={10}>
            <Image
              rounded={'md'}
              alt={'Artistic Representation of Tracking'}
              src={
                '/assets/dashboardart.png'
              }
              objectFit={'cover'}
            />
          </Flex>
        </SimpleGrid>
      </Container>
    );
  }

export default withAuthenticated(Dashboard)