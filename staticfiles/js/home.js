let currentSlide = 0;

const slides = [
  {
    title: "Har Ghar Jal Project",
    description:
      "UDAAN Society is appointed an Implementation support Agency under Jal Jeevan Mission –Har Ghar Jal Project of Govt. of India by State Water and Sanitation Mission, Uttar Pradesh for two District namely Aligarh & Bulandshahr",
    image: "assets/image1.jpeg",
  },
  {
    title: "Atal Bhujal Yojna",
    description:
      "UDAAN society is working as a District Implementation Partner(DIP) under this project in Banda district of Uttar Pradesh and mobilizing the village community to reduce the wastage of water and recharge the ground water such an manner",
    image: "assets/image2.jpeg",
  },
  {
    title: "Women and Child Line",
    description:
      "CHILDLINE 1098 is a phone number that spells hope for millions of children across India",
    image: "assets/image3.jpeg",
  },
  {
    title: "Partnership with AALI",
    description:
      "AALI (Association for Advocacy and Legal Initiatives Trust) is a women-led and women –run organization that works to protect and advance the rights of women",
    image: "assets/image4.jpeg",
  },
  {
    title: "PM Svanidhi Project",
    description:
      "UDAAN Society is Working as an Implementation Agency for Aligarh Nagar Nigam for economic empowerment of street level vendors under Prime Minister Svanidhi Yojana since the year 2021",
    image: "assets/image5.webp",
  },
];

function changeSlide(direction) {
  currentSlide += direction;
  if (currentSlide < 0) currentSlide = slides.length - 1;
  if (currentSlide >= slides.length) currentSlide = 0;
  updateSlide();
}

function goToSlide(index) {
  currentSlide = index;
  updateSlide();
}

function updateSlide() {
  const hero = document.querySelector(".hero");
  const heroContent = document.querySelector(".hero-content");

  heroContent.style.opacity = "0";

  setTimeout(() => {
    // Update text
    document.querySelector(".hero h1").textContent = slides[currentSlide].title;
    document.querySelector(".hero p").textContent =
      slides[currentSlide].description;

    // Update background image
    hero.style.background = `
      linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
      url("${slides[currentSlide].image}") center / cover
    `;

    heroContent.style.opacity = "1";

    document.querySelectorAll(".carousel-dot").forEach((dot, index) => {
      dot.classList.toggle("active", index === currentSlide);
    });
  }, 300);
}

updateSlide();

// Auto-advance slides
setInterval(() => changeSlide(1), 5000);
