import React from "react";
import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { checkUserLoggedIn } from "@/utils/auth";
import { Text } from "@nextui-org/react";
import { Card, Container, Link } from "@nextui-org/react";

export default function ApiKeys() {
    const router = useRouter();
    const [data, setData] = useState(null);
    const [msg, setMsg] = useState(null);

    useEffect(() => {
        checkUserLoggedIn()
            .then((data) => {
                setData(data.user.first_name);
            })
            .catch((error) => {
                router.push("/login");
                console.log(error);
            });
    }, [router]);

    return (
        <>
            <Container gap={2} justify="center">
                <Text h1 align-items="center">
                    API Keys
                </Text>
            </Container>
        </>
    );
}