const hamburgerMenu = document.querySelector('.hamburger-menu');
        const navbarLinks = document.querySelector('.navbar-links');

        hamburgerMenu.addEventListener('click', () => {
            navbarLinks.classList.toggle('active');
        });