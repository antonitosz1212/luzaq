document.addEventListener("DOMContentLoaded", () => {
  const assistantBubble = document.getElementById("chatbot-toggle");
  const chatWindow = document.getElementById("chatbot-window");
  const chatMessages = document.getElementById("chat-messages");
  const userInput = document.getElementById("chat-input");
  const chatForm = document.getElementById("chat-form");
  let inactivityTimer;

  const openSound = new Audio("/static/sounds/open.mp3");
  const closeSound = new Audio("/static/sounds/close.mp3");
  const messageSound = new Audio("/static/sounds/message.mp3");

  assistantBubble.addEventListener("click", toggleChatWindow);

  function toggleChatWindow() {
    if (chatWindow.classList.contains("visible")) {
      chatWindow.classList.remove("fade-in");
      chatWindow.classList.add("fade-out");
      closeSound.play();
      clearTimeout(inactivityTimer);

      chatWindow.addEventListener("transitionend", function handler() {
        chatWindow.classList.remove("visible", "fade-out");
        chatWindow.classList.add("hidden");
        chatWindow.removeEventListener("transitionend", handler);
      });
    } else {
      chatWindow.classList.remove("hidden", "fade-out");
      chatWindow.classList.add("visible");

      requestAnimationFrame(() => {
        chatWindow.classList.add("fade-in");
      });

      openSound.play();
      userInput.focus();
      resetInactivityTimer();

      if (chatMessages.children.length === 0) {
        appendMessage("assistant", "Hola 👋 ¿En qué puedo ayudarte hoy?");
      }
    }
  }

  // FORMULARIO DE CONTACTO
  document.getElementById("contact-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value;
  const email = document.getElementById("email").value;
  const mensaje = document.getElementById("mensaje").value;

  const response = await fetch("/api/contact", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nombre: nombre,
      email: email,
      mensaje: mensaje,
    }),
  });

  const result = await response.json();

  const statusMessage = document.getElementById("status-message");
  if (response.ok) {
    statusMessage.textContent = result.message;
    statusMessage.style.color = "green";
    document.getElementById("contact-form").reset();
  } else {
    statusMessage.textContent = "Ocurrió un error. Inténtalo nuevamente.";
    statusMessage.style.color = "red";
  }
  });

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage("user", text);
    userInput.value = "";
    resetInactivityTimer();

    try {
      const res = await fetch("/chat/respond", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      const answer = data.response;
      appendMessage("assistant", answer);
      messageSound.play();
      highlightSuggested(answer);
    } catch {
      appendMessage("assistant", "Hubo un error al procesar tu pregunta.");
    }
  });

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.textContent = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function highlightSuggested(text) {
    const regex = /#(\w[-\w]*)/g;
    let m;
    while ((m = regex.exec(text)) !== null) {
      const el = document.getElementById(m[1]);
      if (el) {
        el.classList.add("highlight-flash");
        setTimeout(() => el.classList.remove("highlight-flash"), 3000);
      }
    }
  }

  function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
      if (chatWindow.classList.contains("visible")) {
        toggleChatWindow();
      }
    }, 15000);
  }

  userInput.addEventListener("input", resetInactivityTimer);
  chatMessages.addEventListener("scroll", resetInactivityTimer);
});

const style = document.createElement("style");
style.textContent = `
#chatbot-window.fade-in {
  opacity: 1;
  transform: scale(1);
}
#chatbot-window.fade-out {
  opacity: 0;
  transform: scale(0.8);
}
@keyframes flashHighlight {
  0%, 100% { outline-color: transparent; }
  50% { outline-color: #00bcd4; }
}
.highlight-flash {
  animation: flashHighlight 1s ease-in-out 0s 3;
  outline: 3px solid #00bcd4;
  outline-offset: 2px;
  border-radius: 5px;
}`;
document.head.appendChild(style);

// NAVBAR DINÁMICO
document.addEventListener("DOMContentLoaded", () => {
  const navbar = document.querySelector(".navbar");
  const sections = [
    { id: "inicio",    class: "blue"  },
    { id: "inicio1",    class: "blue"  },
    { id: "sobre-nosotros", class: "green" },
    { id: "contacto",  class: "red"   }
  ];

  // Función que revisa scroll y aplica clase
  function onScroll() {
    const scrollY = window.scrollY + window.innerHeight / 3;

    for (let sec of sections) {
      const el = document.getElementById(sec.id);
      const top = el.offsetTop;
      const bottom = top + el.offsetHeight;

      if (scrollY >= top && scrollY < bottom) {
        // removemos otras clases
        navbar.classList.remove(...sections.map(s => s.class));
        // añadimos la que corresponde
        navbar.classList.add(sec.class);
        break;
      }
    }
  }

  window.addEventListener("scroll", onScroll);
  // Una llamada inicial para la sección en la que estamos al cargar
  onScroll();
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.zoomable').forEach(function (img) {
      img.addEventListener('click', function () {
        console.log("Imagen clickeada"); // Confirmamos que esto ocurre

        // Crear overlay
        const overlay = document.createElement('div');
        overlay.className = 'image-modal-overlay';

        // Crear imagen modal
        const modalImg = document.createElement('img');
        modalImg.src = this.src;
        modalImg.className = 'image-modal';

        // Añadir imagen al overlay
        overlay.appendChild(modalImg);

        // Añadir overlay al body
        document.body.appendChild(overlay);

        // Cerrar al hacer clic en el overlay
        overlay.addEventListener('click', function () {
          overlay.remove();
        });
      });
    });
  });

// ZOOM DE IMÁGENES ENTRE HERO Y HERO1
document.addEventListener("DOMContentLoaded", () => {
  const zoomImages = document.querySelectorAll("img.zoomable");

  zoomImages.forEach(img => {
    img.addEventListener("click", () => {
      openImageModal(img.src, img.alt);
    });
  });

  function openImageModal(src, alt) {
    // Evita duplicar el modal si ya existe
    if (document.querySelector(".image-modal-overlay")) return;

    const overlay = document.createElement("div");
    overlay.className = "image-modal-overlay";

    const modalImg = document.createElement("img");
    modalImg.src = src;
    modalImg.alt = alt;
    modalImg.className = "image-modal";

    overlay.appendChild(modalImg);
    document.body.appendChild(overlay);

    // Cerrar al hacer clic fuera
    overlay.addEventListener("click", () => {
      overlay.remove();
    });

    // Cerrar con tecla ESC
    document.addEventListener("keydown", function escHandler(e) {
      if (e.key === "Escape") {
        overlay.remove();
        document.removeEventListener("keydown", escHandler);
      }
    });
  }
});
