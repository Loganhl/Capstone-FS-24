import {Navbar,NavbarBrand,Container,Nav} from 'react-bootstrap'

const Navigation = ()=>{
    return(
        <Navbar>
            <Container>
                <Navbar.Brand href='#'></Navbar.Brand>
            </Container>
            <Nav.Link href='#login'>Login</Nav.Link>
        </Navbar>
    )
}