
import { useAuthContext } from '@/hooks/useAuthContext';
import {
  Container,
  Stack,
  Flex,
  Box,
  Heading,
  Text,
  Button,
  Image,
  Img
} from '@chakra-ui/react';
import { Varela } from '@next/font/google';
import { useRouter } from 'next/router';

export default function Home() {

  const router = useRouter();
  const { currentUser, logOut} = useAuthContext();
  var jobs = 'jobs';
  var analytics = "billing";
  if (!currentUser) {
    jobs = 'login';
    analytics = 'login';
  }

  return (
    <Container maxW={'7xl'}>
      <Stack
        align={'center'}
        spacing={{ base: 8, md: 10 }}
        py={{ base: 20, md: 28 }}
        direction={{ base: 'column', md: 'row' }}>
        <Stack flex={1} spacing={{ base: 5, md: 10 }}>
          <Heading
            lineHeight={1.1}
            fontWeight={600}
            fontSize={{ base: '3xl', sm: '4xl', lg: '6xl' }}>
            <Text
              as={'span'}
              position={'relative'}
              _after={{
                content: "''",
                width: 'full',
                height: '30%',
                position: 'absolute',
                bottom: 1,
                left: 0,
                bg: 'red.400',
                zIndex: -1,
              }}>
              Leave tracking
            </Text>
            <br />
            <Text as={'span'} color={'red.400'}>
              your progress to us
            </Text>
          </Heading>
          <Text color={'gray.500'}>
            Snippy is a rich coding snippets app that lets you create your own
            code snippets, categorize them, and even sync them in the cloud so
            you can use them anywhere. All that is free!
          </Text>
          <Stack
            spacing={{ base: 4, sm: 6 }}
            direction={{ base: 'column', sm: 'row' }}>
            <Button 
              onClick={() => router.push(jobs)}
              rounded={'full'}
              size={'lg'}
              fontWeight={'normal'}
              px={6}
              colorScheme={'red'}
              bg={'red.400'}
              _hover={{ bg: 'red.500' }}>
              Learn More About Jobs
            </Button>
            <Button
               onClick={() => router.push(analytics)}
              rounded={'full'}
              size={'lg'}
              fontWeight={'normal'}
              bg={"#0072f5"}
              _hover={{ bg: '#0164d6' }}
              px={6}>
              Get Started With Analytics
            </Button>
          </Stack>
        </Stack>
        <Flex
          flex={1}
          justify={'center'}
          align={'center'}
          position={'relative'}
          w={'full'}>
          <Box
            position={'relative'}
            height={'300px'}
            rounded={'2xl'}
            boxShadow={'2xl'}
            width={'full'}
            overflow={'hidden'}>
            <Image
              alt={'Jobs Progress Page'}
              fit={'cover'}
              align={'center'}
              src={"/assets/jobs.png"}
            />
          </Box>
        </Flex>
      </Stack>
    </Container>
  );
}
