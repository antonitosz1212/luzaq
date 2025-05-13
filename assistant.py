from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Cargar modelo
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

# GPU si hay
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Información base
contexto_empresa = (
    "Fue fundada en Septiembre del 2007, la misma fecha de inicio de actividades y "
    "tiene su sede en el departamento de Huánuco, distrito de Amarilis; está ubicado " \
    "en la avenida Marcos Durán Martel N° 229."
    "El representante legal de la empresa es la señora Sandra Luz Zuñiga Briceño, quien " \
    "es la Gerente General de la empresa."

    "LUZAQ INGENIEROS S.R.L. es una empresa privada peruana, con sede en Amarilis, "
    "Huánuco, fundada en septiembre de 2007. Está legalmente representada por Sandra "
    "Luz Zuñiga Briceño, quien ejerce el cargo de Gerente General. Desde su inicio, "
    "se ha dedicado a la consultoría, elaboración y ejecución de proyectos de "
    "ingeniería e infraestructura, destacándose por su compromiso con la calidad, "
    "eficiencia, responsabilidad ambiental y desarrollo regional."

    "La misión de LUZAQ se enfoca en ofrecer servicios de ingeniería e infraestructura "
    "que superen las expectativas contractuales de sus clientes, trabajando en "
    "armonía con el medio ambiente y las comunidades locales. Promueven un entorno "
    "laboral que valora el crecimiento personal y profesional de su equipo humano. " \
    "Sus pilares fundamentales son la orientación al cliente, que consiste en "
    "ofrecer soluciones de ingeniería y construcción que superen las expectativas; " \
    "La rentabilidad sostenible, que genera ganancias para crecer de forma sólida y "
    "retribuir a sus accionistas; y el desarrollo del equipo, para fomentar el "
    "bienestar y la realización personal de sus colaboradores."

    "Su visión es Ser reconocida como la empresa de consultoría y ejecución más "
    "confiable y eficiente de la región, garantizando proyectos de alta calidad, "
    "con precios competitivos y en plazos óptimos, gracias al compromiso y "
    "profesionalismo de su personal. " \
    "Destacando por sus servicios integrales (ingeniería, abastecimiento de "
    "materiales y construcción); sus equipos de trabajo multidisciplinarios, "
    "motivados y éticos; y por la mejora continua de procesos para ofrecer mejores "
    "precios, plazos y calidad."

    "LUZAQ INGENIEROS es una empresa sólida y experimentada en el campo de la "
    "ingeniería civil en el Perú, destacada por su profesionalismo, cumplimiento, y "
    "su capacidad para desarrollar tanto proyectos públicos como privados. Su "
    "enfoque centrado en la calidad y la mejora continua le ha permitido posicionarse "
    "como un actor confiable en el desarrollo regional, especialmente en Huánuco y "
    "otras zonas del centro del país."

    "LUZAQ INGENIEROS S.R.L. es una empresa confiable, con experiencia comprobada "
    "y recursos adecuados para proyectos de ingeniería y construcción de diversa "
    "escala.\n\n"
)

# Diccionario de respuestas fijas
respuestas_rapidas = {
    "¿cuál es el horario de atención?": "Nuestro horario es de lunes a viernes de 8:00 a 18:00.",
    "¿dónde están ubicados?": "Tenemos oficinas en Lima, Bogotá, Ciudad de México, Madrid y Tokio.",
    "¿cómo puedo contactarlos?": "Puedes escribirnos a contacto@luzaq.com o llamarnos al +51 1 234 5678.",
    "¿qué servicios ofrecen?": "Ofrecemos servicios de ingeniería civil, infraestructura, planificación urbana y consultoría técnica.",
    "¿tienen redes sociales?": "Sí, estamos en LinkedIn, Facebook y Twitter como @LuzaqIngenieros.",
    "¿cuál es su enfoque en sostenibilidad?": "Nos comprometemos a realizar proyectos sostenibles y respetuosos con el medio ambiente.",
    "¿tienen proyectos en el extranjero?": "Sí, hemos trabajado en proyectos en América, Europa y Asia.",
    "¿cómo puedo enviar mi CV?": "Puedes enviar tu CV a la dirección de correo electrónico",
    "¿tienen programas de pasantías?": "Sí, ofrecemos programas de pasantías para estudiantes de ingeniería.",
    "¿qué tipo de proyectos realizan?": "Realizamos proyectos de infraestructura, obras civiles y planificación urbana.",
    "¿tienen certificaciones?": "Sí, contamos con certificaciones ISO 9001, ISO 14001 y OHSAS 18001.",
    "¿cómo es el proceso de selección?": "El proceso de selección incluye una revisión de CV, entrevistas y pruebas técnicas.",
    "¿qué beneficios ofrecen a sus empleados?": "Ofrecemos beneficios como seguro médico, capacitaciones y oportunidades de crecimiento.",
    "¿tienen algún programa de responsabilidad social?": "Sí, participamos en proyectos de responsabilidad social en comunidades locales.",
    "¿cómo puedo hacer una consulta técnica?": "Puedes enviarnos un correo a",
    "¿tienen algún proyecto destacado?": "Sí, hemos trabajado en proyectos como el Metro de Lima y la ampliación del Aeropuerto de Bogotá.",
    "¿qué idiomas hablan en la empresa?": "En la empresa hablamos español, inglés y portugués.",
    "¿tienen algún programa de capacitación?": "Sí, ofrecemos programas de capacitación continua para nuestros empleados.",
    "¿cómo es el ambiente laboral?": "Fomentamos un ambiente colaborativo y de respeto entre todos los empleados.",
    "¿tienen algún programa de bienestar?": "Sí, contamos con programas de bienestar y salud para nuestros empleados.",
    "¿cómo puedo hacer una queja?": "Puedes enviar tu queja al correo electrónico de recursos humanos.",
    "¿cómo puedo hacer un reclamo?": "Puedes enviar tu reclamo al correo electrónico de atención al cliente.",
    "¿tienen algún programa de diversidad e inclusión?": "Sí, promovemos la diversidad y la inclusión en nuestro equipo.",
    "¿cómo puedo hacer una sugerencia?": "Puedes enviar tu sugerencia al correo electrónico de atención al cliente.",
    "¿tienen algún programa de reconocimiento?": "Sí, contamos con programas de reconocimiento para nuestros empleados destacados.",
    "¿cómo puedo obtener una cotización?": "Puedes solicitar una cotización enviando un correo a",
    "¿tienen algún programa de fidelización?": "Sí, ofrecemos programas de fidelización para nuestros clientes frecuentes.",
    "¿cómo puedo hacer un seguimiento a mi consulta?": "Puedes hacer seguimiento enviando un correo a",
    "¿tienen algún programa de referidos?": "Sí, contamos con un programa de referidos para nuestros empleados.",
    "¿cómo puedo hacer una consulta sobre un proyecto?": "Puedes enviar tu consulta al correo electrónico de atención al cliente.",
    "¿tienen algún programa de innovación?": "Sí, promovemos la innovación en nuestros proyectos y procesos.",
    "¿cómo puedo hacer una consulta sobre un servicio?": "Puedes enviar tu consulta al correo electrónico de atención al cliente.",
}

def get_response(prompt: str) -> str:
    try:
        pregunta = prompt.lower().strip()

        # Primero, intentamos respuesta fija
        for clave, respuesta in respuestas_rapidas.items():
            if clave in pregunta:
                print(f"[DEBUG] Respuesta directa encontrada para: {clave}")
                return respuesta

        # Si no hay respuesta fija, generamos con el modelo
        full_prompt = (
            contexto_empresa +
            "Responde como un asistente profesional en español. Sé claro, útil y conversacional.\n\n"
            f"Pregunta: {prompt}\n\n"
            "Respuesta:"
        )

        input_ids = tokenizer(full_prompt, return_tensors="pt").input_ids.to(device)
        outputs = model.generate(
            input_ids,
            max_length=250,
            num_beams=4,            # Coherencia
            no_repeat_ngram_size=2,
            early_stopping=True
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        print(f"[DEBUG] Prompt recibido: {prompt}")
        print(f"[DEBUG] Respuesta generada: {response}")

        return response if response else "Lo siento, no tengo una respuesta clara para eso."

    except Exception as e:
        print(f"[ERROR al generar respuesta]: {e}")
        return "Ocurrió un error al generar la respuesta."