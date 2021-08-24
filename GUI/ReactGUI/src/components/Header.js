import logo from '../resources/Logo.png'

const Header = () => {
    return (
        <header className="site-header" id="header">
            <div className="site-identity">
                <img alt='' src={logo} />
                <h1><a href="#header">Pathfinding Algorithms demo</a></h1>
            </div>
            <nav className="site-navigation">
                <ul className="nav">
                    <li><a href="#header">About</a></li>
                    <li><a href="#header">News</a></li>
                    <li><a href="#header">Contact</a></li>
                </ul>
            </nav>
        </header>
    )
}

export default Header