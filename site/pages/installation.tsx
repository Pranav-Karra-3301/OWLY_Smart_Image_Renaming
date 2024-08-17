import styled from 'styled-components';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  color: #1c1c1e;
  margin-bottom: 1.5rem;
  text-align: center;
`;

const Content = styled.div`
  font-size: 1.125rem;
  color: #3a3a3a;
  line-height: 1.8;
  & h2 {
    margin-top: 2rem;
    font-size: 1.75rem;
  }
  & p, & ul, & code {
    margin-top: 1rem;
  }
`;

export default function Installation() {
  return (
    <Container>
      <Title>Installation & Usage</Title>
      <Content>
        {/* Replace with the actual Installation and Usage content from your README */}
        <h2>Installation</h2>
        <p>To install the project, follow these steps...</p>
        <code>
          npm install <br />
          npm start
        </code>
        <h2>Usage</h2>
        <p>To use the project, follow these steps...</p>
      </Content>
    </Container>
  );
}