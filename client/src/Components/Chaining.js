import '../Component.css';

const Chaining = props => {
    return (
        <>
        <nav style={{borderBottom: '2px groove #284B63'}} className="pl-2 pt-0 navbar navbar-expand-lg bg-primary">
            <div className="container-fluid">
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <h5 className="text-secondary ml-4 pt-0 mb-0">Target URL : &nbsp;&nbsp;<a className="text-secondary" target="_blank" rel="noreferrer" href={urls[0]}>{urls[0]}</a></h5>
                </div>
            </div>
        </nav>
        <div className="bg-secondary checklistStyle ml-4">
            <ul>
                <li>Reflected Input</li>
                <ul>
                    <li>Cross-Site Scripting (XSS)</li>
                    <ul>
                        <li>CORS Bypass</li>
                        <li>Session Riding</li>
                    </ul>
                </ul>
                <li>Open Redirect</li>
                <ul>
                    <li>Different Paths</li>
                    <li>Different Subdomains</li>
                    <li>Different FQDN</li>
                </ul>    
            </ul>
        </div>
        <div className="bg-secondary workTableStyle">
        </div>
        </>
    )
}

export default Chaining;