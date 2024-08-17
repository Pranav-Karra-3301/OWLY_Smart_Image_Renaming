import Link from 'next/link';
import styled from 'styled-components';

const Nav = styled.nav`
  display: flex;
  justify-content: center;
  padding: 1rem;
  background-color: #f5f5f7;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const NavLink = styled.a`
  margin: 0 1rem;
  font-size: 1.125rem;
  color: #0070f3;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
`;

export default function Navigation() {
  return (
    <Nav>
      <Link href="/" passHref>
        <NavLink>Home</NavLink>
      </Link>
      <Link href="/roadmap" passHref>
        <NavLink>Roadmap</NavLink>
      </Link>
      <Link href="/installation" passHref>
        <NavLink>Installation & Usage</NavLink>
      </Link>
      <Link href="/license" passHref>
        <NavLink>License</NavLink>
      </Link>
    </Nav>
  );
}