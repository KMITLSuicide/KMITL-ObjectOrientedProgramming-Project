import Logo from "./logo";

import MdiAccountCircle from '~icons/mdi/account-circle';

export default function NavBar() {
    return(
        <nav className="w-auto bg-slate-900 text-white p-6 flex gap-4">
            <Logo />
            <div className="flex-grow" />
            <p>one</p>
            <p>two</p>
            <MdiAccountCircle   />
        </nav>
    );
}