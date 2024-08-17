import Link from 'next/link';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const Container = styled(motion.div)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 0 2rem;
  background: linear-gradient(180deg, #ffffff, #f5f5f7);
`;

const Title = styled(motion.h1)`
  font-size: 4rem;
  text-align: center;
  color: #1c1c1e;
`;

const Description = styled(motion.p)`
  font-size: 1.5rem;
  text-align: center;
  color: #6e6e73;
  margin-top: 1rem;
`;

const GitHubButton = styled(motion.a)`
  margin-top: 2rem;
  font-size: 1.25rem;
  padding: 0.75rem 1.5rem;
  color: #ffffff;
  background-color: #0070f3;
  border-radius: 5px;
  text-decoration: none;
  cursor: pointer;
  &:hover {
    background-color: #005bb5;
  }
`;

export default function Home() {
  return (
    <Container
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.5 }}
    >
      <Title
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1.2, delay: 0.3 }}
      >
        Welcome to My Project
      </Title>
      <Description
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1.2, delay: 0.6 }}
      >
        {/* Replace with the introduction from your README */}
        This project is designed to showcase advanced features in web development, including...
      </Description>
      <GitHubButton
        href="https://github.com/your-username/your-repo-name"
        target="_blank"
        rel="noopener noreferrer"
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1.2, delay: 0.9 }}
      >
        View on GitHub
      </GitHubButton>
    </Container>
  );
}