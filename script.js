
const faders = document.querySelectorAll('.fade-in');

    const appearOptions = {
      threshold: 0.5,
      rootMargin: "0px 0px -50px 0px"
    };

    const appearOnScroll = new IntersectionObserver((entries, appearOnScroll) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) {
          return;
        } else {
          entry.target.classList.add('visible');
          appearOnScroll.unobserve(entry.target);
        }
      });
    }, appearOptions);

    faders.forEach(fader => {
      appearOnScroll.observe(fader);
    });

    const testimonials = [
        { name: "John Perry", text: "FOODWIZ has transformed my cooking routine. The personalized recipes..." },
        { name: "Jane Doe", text: "I never thought cooking could be this easy! The personalized recipes..." },
        { name: "Tom Smith", text: "The variety of recipes has helped me explore new cuisines and ingredients..." },
        { name: "Sarah Connor", text: "The AI-generated recipes are spot-on with my preferences, and I love..." },
        { name: "Alex Brown", text: "I've been able to cook healthier meals thanks to the personalized recipe..." }
    ];

    function showTestimonial(index) {
        document.getElementById("testimonial-name").innerText = testimonials[index].name;
        document.getElementById("testimonial-text").innerText = testimonials[index].text;
    }

    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");
    const closeMenu = document.getElementById("close-menu");
 
    menuToggle.addEventListener("click", () => {
       sidebar.classList.toggle("-translate-x-full");
    });
 
    closeMenu.addEventListener("click", () => {
       sidebar.classList.add("-translate-x-full");
    });
    let currentIndex = 0;
    const slides = document.querySelectorAll('.slide');
    
    function showSlide(index) {
      const totalSlides = slides.length;
      if (index >= totalSlides) {
        currentIndex = 0;
      } else if (index < 0) {
        currentIndex = totalSlides - 1;
      } else {
        currentIndex = index;
      }
      const offset = -currentIndex * 100;
      document.querySelector('.slides').style.transform = `translateX(${offset}%)`;
    }
    
    setInterval(() => {
      showSlide(currentIndex + 1);
    }, 3000);

    require('dotenv').config();
    const API_KEY = process.env.SPOONACULAR_API_KEY;
    
