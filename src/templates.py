NICHES = {}

def niche(name, description, category, prompt_templates, variables):
    NICHES[name] = {
        "name": name,
        "description": description,
        "category": category,
        "prompts": prompt_templates,
        "variables": variables,
    }

niche("medical", "Conversaciones y consultas médico-paciente con lenguaje natural e imperfecciones realistas",
    "salud", [
        "Genera un diálogo entre médico y paciente en español. El paciente de {age} años consulta por {condition}. Incluye: el paciente confunde síntomas con algo que vio en internet, el médico interrumpe brevemente por una llamada, el paciente usa un modismo de {country}, el médico da indicaciones con lenguaje coloquial. La conversación debe sentirse real, con frases incompletas y dudas.",
        "Escribe una nota clínica informal de un médico sobre un paciente con {condition}. El médico añade comentarios personales entre paréntesis, menciona que el paciente trajo un remedio casero absurdo, y escribe alguna abreviatura no estándar que se entiende por contexto. Incluye una recomendación final que suene a consejo de amigo más que a prescripción médica.",
        "Genera una conversación telefónica entre un paciente y una recepcionista de consultorio. El paciente quiere agendar por {condition} pero cuenta toda su historia de vida sin filtro. La recepcionista intenta mantener profesionalismo pero se desconcierta. Incluye ruido de fondo (tecleo, niños, tráfico) mencionado implícitamente, y una cita que se agenda para una fecha graciosa.",
        "Escribe la transcripción de una videollamada médica donde el paciente tiene problemas técnicos y el médico tiene mala conexión. El paciente describe {condition} de forma desorganizada, el médico pide aclaraciones, y al final descubren que el problema real es diferente. Incluye Frustración tecnológica y un desenlace inesperado pero creíble.",
        "Genera un diálogo en una farmacia donde un paciente pide medicamento para {condition} pero no recuerda el nombre. Describe los síntomas con vergüenza, el farmacéutico hace preguntas para ayudar, y hay una confusión con un producto similar. Incluye la intervención de otro cliente que opina sin que le pregunten.",
        "Escribe la entrada del diario personal de un médico al final de un día agotador. Describe tres casos breves incluyendo uno de {condition}. El médico usa jerga mezclada con lenguaje coloquial, olvida escribir alguna palabra, y termina con una reflexión personal que revela agotamiento emocional.",
    ], {
        "condition": ["diabetes tipo 2", "hipertensión arterial", "migraña crónica", "lumbalgia", "ansiedad generalizada", "insomnio", "gastritis", "artritis reumatoide", "hipotiroidismo", "alergias estacionales", "infección urinaria", "dermatitis atópica", "colon irritable", "vértigo", "depresión mayor"],
        "age": list(range(18, 82)),
        "country": ["México", "Colombia", "Argentina", "Chile", "Perú", "España", "Venezuela", "Ecuador", "Uruguay", "Costa Rica"],
    }
)

niche("tech_support", "Tickets y conversaciones de soporte técnico realistas con usuarios frustrados",
    "tecnología", [
        "Escribe un ticket de soporte técnico donde un usuario reporta que {software} dejó de funcionar después de una actualización. El usuario: confunde el sistema operativo, menciona una versión que no existe, adjunta mentalmente un error que vio una vez, y expresa frustración con mayúsculas variables. El técnico responde con una solución genérica que el usuario ya intentó.",
        "Genera un chat de soporte en vivo. El usuario tiene problemas con {software} y el agente sigue un guion rígido. El usuario se desvía contando un problema personal no relacionado. El agente se confunde momentáneamente. Incluye: tiempos de espera, frases cortadas, y una solución antiintuitiva que termina funcionando.",
        "Crea un hilo de foro de soporte comunitario donde un usuario pide ayuda con {software}. Otro usuario responde con una solución incorrecta pero segura. Un tercero corrige con tono pasivo-agresivo. El OP vuelve días después a agradecer y reportar que funcionó parcialmente.",
        "Escribe un correo de soporte técnico de un usuario furioso que lleva una semana sin resolver {software}. Incluye: reclamo sobre el tiempo de espera, mención a un competidor, una solución rara que encontró en YouTube, y una petición de escalación amenazante pero sin consecuencias reales.",
        "Genera una conversación de Slack/Discord en un canal de soporte técnico. Tres personas intentan ayudar a una cuarta con {software}. Hay un malentendido porque usan jerga diferente. Alguien comparte un meme. La solución termina siendo reiniciar todo.",
        "Ticket de soporte de un usuario de 60+ años que no sabe explicar el problema con {software}. Describe lo que ve en pantalla con metáforas físicas (como 'la ventanita se fue volando'). El técnico intenta traducir a términos técnicos. Incluye paciencia y confusión mutua.",
    ], {
        "software": ["Microsoft Teams", "SAP", "Salesforce", "QuickBooks", "Slack", "Zoom", "Notion", "Trello", "Jira", "Google Workspace", "Adobe Acrobat", "Windows 11", "macOS Ventura", "Linux Ubuntu"],
    }
)

niche("local_reviews", "Reseñas de productos y servicios con sabor local y autenticidad",
    "opiniones", [
        "Escribe la reseña de un {product} comprado en {city}. El autor: menciona un evento local reciente como contexto, confunde el modelo con otro similar, se queja del empaque pero admite que el producto funciona bien, y escribe con errores de ortografía por escribir rápido desde el celular. Usa modismos de {country}.",
        "Reseña de un servicio en {city} donde el autor se equivoca en la ubicación o el horario. Incluye: comparación implícita con un competidor, una anécdota personal graciosa sobre cómo conoció el lugar, y una contradicción (recomienda pero pone 3 estrellas). Escrita con signos de puntuación inconsistentes.",
        "Genera una reseña en Google Maps de un restaurante en {city}. El cliente: pidió algo que no era lo que pensaba, confunde el nombre del plato, menciona el precio con indignación, incluye una historia sobre su acompañante, y termina diciendo que volverá. Escrita toda en minúsculas con emojis.",
        "Reseña de producto tecnológico {product}: el usuario confunde especificaciones técnicas (MHz por GHz, GB por Gb). Menciona que se lo recomendó un amigo que 'sabe de esto'. Compara con la competencia sin nombrarla. Dice que el manual es inútil. Tono entre frustrado y resignado.",
        "Reseña de un producto de belleza o salud {product}: el usuario lo usó dos veces y ya 'notó resultados increíbles'. Lenguaje de testimonio de infomercial. Menciona que su {relative} también lo usa. Incluye una queja irrelevante sobre el olor o el color. Exclamaciones excesivas.",
        "Reseña en Amazon de {product} donde el usuario hizo un review extremadamente detallado con fotos mentales. Incluye: mediciones caseras, comparación con una marca blanca, teoría conspirativa sobre el empaque, recomendación final ambigua. Escrita como si el reviewer fuera ingeniero sin serlo.",
    ], {
        "product": ["licuadora Ninja", "iPhone 16", "suplemento de colágeno", "zapatos ortopédicos", "smart TV Hisense", "aspiradora robot", "cafetera espresso", "audífonos Bluetooth", "colchón viscoelástico", "crema antiedad", "sartén antiadherente", "pantalones de yoga", "proteína vegetal", "lámpara inteligente", "mochila para laptop"],
        "city": ["Ciudad de México", "Bogotá", "Buenos Aires", "Lima", "Santiago de Chile", "Medellín", "Guadalajara", "Monterrey", "Quito", "Caracas", "La Paz", "San José"],
        "country": ["México", "Colombia", "Argentina", "Perú", "Chile", "Venezuela", "Ecuador", "Costa Rica", "Bolivia", "Uruguay"],
        "relative": ["mamá", "papá", "abuelo", "hermana", "cuñado", "vecino", "suegra", "tía"],
    }
)

niche("legal_consultation", "Consultas legales expresadas en lenguaje cotidiano, no técnico",
    "legal", [
        "Escribe la consulta de un cliente a un abogado explicando su caso de {legal_issue}. El cliente: usa terminología legal incorrecta, se desvía contando detalles irrelevantes, menciona que 'vio algo parecido en una serie', y expresa preocupación por los costos. El abogado responde en lenguaje claro con una advertencia informal.",
        "Genera un diálogo en un juzgado de {city} donde una persona declara sobre {legal_issue}. El declarante contradice su propia declaración, usa modismos locales, y el juez tiene que pedirle que se centre. Incluye un momento de tensión que se resuelve con una broma del secretario.",
        "Correo de un cliente a su abogado: 'Le mando esto urgente...' explicando {legal_issue} entremezclado con problemas personales. El cliente adjuntó capturas de pantalla en lugar de documentos. Incluye cinco intentos de explicar lo mismo de diferentes maneras. Firma con nombre y apodo.",
        "Consulta en red social tipo 'alguien sabe de leyes?' sobre {legal_issue}. Recibe respuestas de: un estudiante de derecho confiado, alguien que 'le pasó exactamente lo mismo', y un abogado real que corrige a todos con paciencia. El OP agradece pero sigue confundido.",
        "Transcripción de llamada a un bufete de abogados. La recepcionista intenta categorizar {legal_issue} pero el cliente insiste en contar todo desde el principio. Incluye: música de espera mencionada, una interrupción por el delivery del cliente, y una cita agendada para la fecha incorrecta.",
    ], {
        "legal_issue": ["divorcio conflictivo", "herencia disputada", "despido injustificado", "accidente de tránsito", "problema de arrendamiento", "estafa por internet", "incumplimiento de contrato", "cobro de deudas", "custodia de hijos", "propiedad intelectual"],
        "city": ["Ciudad de México", "Bogotá", "Buenos Aires", "Lima", "Madrid", "Santiago", "Montevideo"],
    }
)

niche("financial_advice", "Conversaciones sobre finanzas personales con lenguaje cotidiano",
    "finanzas", [
        "Un usuario en un foro de finanzas personales pregunta cómo ahorrar para {financial_goal}. Cuenta su situación: gana X, gasta en Y, tiene deuda de Z. Otros usuarios responden con: un plan estricto, un consejo heterodoxo, y alguien que recomienda criptomonedas sin que pregunten. El OP defiende sus gastos.",
        "Escribe una conversación entre un asesor financiero y un cliente que quiere {financial_goal}. El cliente: confunde conceptos básicos (acciones con bonos), revela información personal innecesaria, y menciona un 'tip' que le dio un amigo. El asesor simplifica pero se nota frustrado.",
        "Diálogo en una familia sobre finanzas: los {relative} discuten cómo ayudar a un familiar con {financial_goal}. Cada uno tiene una opinión distinta: uno prefiere ahorrar, otro invertir, otro 'que se arregle solo'. Incluye: referencias a crisis pasadas, una comparación con el vecino, y un acuerdo parcial al final.",
        "Post de TikTok/Reel transcrito: 'Chicos, les voy a explicar cómo lograr {financial_goal} en 3 pasos... pero primero mi historia'. La persona cuenta una anécdota personal de deudas, da consejos contradictorios, y termina promocionando un producto. Escrito con muletillas y repeticiones.",
        "Entrada en un diario de finanzas personales. La persona escribe sobre su progreso hacia {financial_goal}. Incluye: un gasto emocional que justifica, un cálculo matemático incorrecto, una resolución que ya rompió, y esperanza renovada. Escrito con mezcla de orgullo y culpa.",
    ], {
        "financial_goal": ["comprar una casa", "ahorrar para la universidad", "invertir por primera vez", "saldar deudas de tarjeta", "crear un fondo de emergencia", "emprender un negocio", "viajar por un año", "adelantar el hipotecario"],
        "relative": ["hermanos", "primos", "cuñados", "tíos", "papás"],
    }
)

niche("educational_tutoring", "Sesiones de tutoría educativa con dinámica profesor-alumno realista",
    "educación", [
        "Escribe una sesión de tutoría virtual sobre {subject}. El estudiante: confunde conceptos básicos, hace una pregunta que no viene al caso, y se queja de que el profesor de la escuela no explica bien. El tutor explica con ejemplos cotidianos y termina preguntando 'va quedando más claro?'. Incluye: ruido de fondo, pausas, tartamudeos.",
        "Fragmento de un grupo de WhatsApp de estudiantes sobre {subject}. Un compañero explica un tema a otro. Hay: malentendidos, capturas de pantalla mal hechas, emojis, un chiste interno, alguien que pregunta lo mismo que ya respondieron, y el profesor que aparece y corrige todo.",
        "Transcripción de una clase grabada de {subject}. El profesor: se desvía contando una anécdota personal, olvida lo que iba a decir, escribe mal en el pizarrón, y retoma el tema con 'como les decía...'. Los estudiantes: hacen preguntas que revelan que no leyeron la lectura, y uno ronca y se despierta.",
        "Un estudiante escribe en un foro de ayuda con {subject}. Describe su problema con terminología inexacta. Responde a su propio post dos veces: primero con 'ya me salió' y luego con 'no, no me salió'. Un tutor responde con una guía paso a paso que el estudiante ignora parcialmente.",
        "Conversación de tutoría presencial en una biblioteca. El tutor explica {subject} usando objetos cotidianos como metáfora. El estudiante: tiene un momento de revelación pero luego vuelve a confundirse, pregunta 'y esto para qué sirve en la vida real?', y agradece efusivamente al final.",
    ], {
        "subject": ["álgebra lineal", "química orgánica", "gramática española", "programación en Python", "física mecánica", "historia universal", "redacción académica", "estadística básica", "inglés intermedio", "contabilidad", "trigonometría", "biología celular"],
    }
)

niche("therapy_session", "Fragmentos de sesiones de terapia con lenguaje coloquial y emociones genuinas",
    "salud mental", [
        "Fragmento de una sesión de terapia. El paciente habla de su {anxiety_topic} pero evade el tema principal contando detalles triviales. El terapeuta hace una pregunta que lo desconcierta. El paciente: se ríe nerviosamente, hace una pausa larga, y revela algo profundo casi sin querer. Finaliza con un 'no sé...'.",
        "Diario personal de alguien que empieza terapia. Escribe sobre su primera sesión: llegó con una lista mental de temas para {anxiety_topic} pero terminó hablando de otra cosa. Describe al terapeuta con detalles físicos irrelevantes. Reflexiona sobre si 'esto realmente funciona'. Incluye dudas y esperanza entremezcladas.",
        "Conversación de WhatsApp entre amigues después de una sesión de terapia. La persona procesa lo que habló sobre {anxiety_topic}. Alterna entre: revelaciones profundas, memes para aliviar la tensión, preguntas existenciales, y planes banales para la cena. Sus amigues responden con apoyo y humor.",
        "Un post en Reddit de alguien que pregunta 'alguien más siente X cuando...' sobre {anxiety_topic}. Cuenta su experiencia con detalles muy específicos. Los comentarios son: alguien que se identifica totalmente, alguien que da un consejo no solicitado, y alguien que comparte su historia más extrema.",
        "Escribe la entrada de un terapeuta en sus notas clínicas informales después de una sesión intensa sobre {anxiety_topic}. Mezcla observaciones profesionales con reacciones personales entre paréntesis. Se da cuenta de algo sobre su propio sesgo. Termina con un recordatorio para investigar algo. Escrito en un estilo entre formal y humano.",
    ], {
        "anxiety_topic": ["ansiedad social", "síndrome del impostor", "miedo al fracaso", "duelo no procesado", "problemas de pareja", "estrés laboral", "autoestima", "relaciones familiares", "procrastinación crónica", "crisis de identidad"],
    }
)

niche("customer_service", "Interacciones de servicio al cliente con todo tipo de clientes",
    "atención al cliente", [
        "Chat de servicio al cliente. El cliente contacta por {product_issue} pero su queja real es más profunda. El agente sigue el protocolo mientras el cliente se calienta. Incluye: tiempos de espera, frases de cortesía vacías, y una solución que el cliente rechaza tres veces antes de aceptar.",
        "Llamada telefónica a servicio al cliente. El cliente: no sabe su número de cuenta, habla a gritos sin razón, interrumpe al agente, y revela accidentalmente que no leyó el manual. El agente mantiene la calma pero su tono se vuelve cada vez más plano. Resolución anticlimática.",
        "Escribe un correo de queja formal pero escrito a las 2am. El cliente está frustrado por {product_issue}, mezcla enojo con vulnerabilidad, admite que 'quizás yo hice algo mal' pero luego se retracta. Incluye: múltiples borradores visibles en el mismo correo, mayúsculas erráticas, y una posdata que cambia el tono.",
        "Transcripción de redes sociales: una queja pública sobre {product_issue} se vuelve viral en comentarios. La empresa responde con el mismo copy-paste tres veces. Otros usuarios intervienen: unos defienden a la marca, otros cuentan sus propias historias, uno hace un chiste. El OP actualiza con 'ya lo resolvieron'. ",
        "Interacción en persona (descrita por el cliente después): cliente va a tienda por {product_issue}. Describe al vendedor con detalles exagerados. Incluye: malentendidos por diferencias generacionales, el vendedor llama a un compañero 'que sabe más', y el problema se resuelve con algo que el cliente 'ya había intentado'.",
    ], {
        "product_issue": ["producto defectuoso", "envío tardío", "facturación incorrecta", "suscripción no cancelada", "garantía no cubierta", "devolución rechazada", "atención al cliente previa", "producto diferente al pedido"],
    }
)

niche("dev_discussion", "Discusiones de desarrollo de software con jerga técnica y humana",
    "tecnología", [
        "Hilo en Stack Overflow (o similar) donde un dev pregunta por {dev_topic}. Publica un código con errores obvios. La respuesta aceptada: funciona pero el OP no entiende por qué. Un comentario señala una micro-optimización irrelevante. OP acepta y se va. Otro dev llega 3 años después y agradece.",
        "Conversación en una daily meeting de desarrollo. El equipo habla de {dev_topic}. Un dev: se extiende en detalles técnicos que nadie sigue, otro está en mute y no se da cuenta, el líder intenta resumir pero empeora. Incluye: referencias a código legacy con resentimiento, y estimaciones incorrectas.",
        "Chat de un equipo de desarrollo resolviendo {dev_topic} a las 11pm. Alternan entre: soluciones técnicas serias, memes, darse ánimo, preguntas existenciales sobre sus elecciones de carrera, y encontrar el bug después de 3 horas. Alguien menciona 'y si lo apagamos y lo encendemos?'.",
        "Post en blog personal de un dev sobre {dev_topic}. Empieza con una introducción estructurada pero se desvía en una discusión sobre por qué odia cierta tecnología. Incluye: analogías forzadas con la cocina, un fragmento de código que no compila, y una conclusión apresurada porque se le hizo tarde.",
        "Pull request review discussion sobre {dev_topic}. El revisor: pide cambios que contradice después, sugiere un patrón de diseño del que no sabe el nombre exacto, y aprueba con 'LGTM' después de 15 comentarios. El autor: defiende su enfoque, cede en cosas menores, y arregla lo importante.",
        "Un dev escribe en Twitter/X sobre {dev_topic}: 'nadie: ... absolutamente nadie: ... el nuevo framework: *hace algo básico* la comunidad: 😍'. Hilo de respuestas: gente que se ofende, gente que está de acuerdo, y un link a una librería que hace lo mismo pero mejor.",
    ], {
        "dev_topic": ["migrar a microservicios", "elegir base de datos", "deuda técnica", "code review", "tests unitarios vs integración", "Docker en producción", "arquitectura limpia", "API REST vs GraphQL", "TypeScript o JavaScript", "CI/CD pipeline", "manejo de estado", "seguridad en APIs"],
    }
)

niche("academic_writing", "Textos académicos con estilo humano, revisiones y retroalimentación",
    "educación", [
        "Escribe el borrador de un ensayo académico sobre {academic_topic}. El autor: cambia de opinión a mitad del párrafo, usa una cita que recuerda a medias, incluye un comentario personal entre corchetes como [esto no sé si va aquí]. Tono entre formal y conversacional. Notas al pie que son más largas que el texto.",
        "Correo entre un profesor y un estudiante sobre el trabajo de {academic_topic}. El estudiante: adjunta el archivo equivocado, pide una extensión con excusa creativa, y formula una pregunta que revela que no entendió la consigna. El profesor: responde con correcciones detalladas y un dejo de cansancio.",
        "Anotaciones de un revisor/relectura de un artículo sobre {academic_topic}. Mezcla: comentarios académicos profundos con 'esto no me gusta' sin explicación, correcciones ortográficas, y preguntas retóricas al autor. Al final escribe 'sugiero aceptar con revisiones menores' después de 40 correcciones mayores.",
        "Discusión en un grupo de estudio universitario sobre {academic_topic}. Los estudiantes: explican conceptos con ejemplos de la cultura pop, se confunden mutuamente, tienen un momento de claridad colectiva, y luego alguien pregunta 'esto va a venir en el examen?'. Incluye ansiedad colectiva y solidaridad académica.",
        "Publicación en un foro académico: 'Alguien tiene el PDF de...?' sobre {academic_topic}. Comentarios: un link caído, alguien que ofrece compartirlo por DM, y un debate tangencial sobre acceso abierto. El OP vuelve 2 meses después a agradecer porque ya se graduó.",
    ], {
        "academic_topic": ["cambio climático y política ambiental", "inteligencia artificial ética", "literatura latinoamericana contemporánea", "desigualdad económica post-pandemia", "neurociencia del aprendizaje", "filosofía de la ciencia", "sociología urbana", "lingüística aplicada", "historia colonial", "bioética"],
    }
)

niche("business_email", "Correos empresariales con errores realistas y dinámicas de oficina",
    "negocios", [
        "Escribe un hilo de correo empresarial sobre {biz_topic}. Empieza con una solicitud clara, pero se va complicando con: respuestas a todos sin necesidad, alguien que adjunta el archivo incorrecto, una discusión paralela sobre quién debería hacer qué, y un 'lo reenvío porque se me fue' al final.",
        "Correo de un empleado a su jefe sobre {biz_topic}. El empleado: usa vocabulario corporativo mal empleado, da demasiado contexto innecesario, pide aprobación para algo que ya hizo, y termina con una frase pasivo-agresiva sutil. El jefe responde 2 semanas después con un 'ok'. ",
        "Invitación a reunión sobre {biz_topic} que debió ser un correo. Hilo de respuestas: '¿es necesario reunirnos?', 'no puedo a esa hora', 'podemos hacerla de 30 min?', 'yo invito el café'. La reunión termina siendo una decisión que ya estaba tomada. Alguien grabó y nadie vio la grabación.",
        "Correo de renuncia inesperado que menciona {biz_topic} como razón de fondo. Tono entre profesional y emocional. Incluye: agradecimiento genérico, crítica velada, promesa de 'dejar todo en orden', y una petición de carta de recomendación. Respuestas del equipo: desde formales hasta un 'nooooo te vayas'.",
        "Cadena de correos navideños empresariales sobre {biz_topic}. Alguien responde a todos con un meme. Otro pide que no respondan a todos pero lo hace respondiendo a todos. El jefe intenta retomar el tema serio pero ya nadie lee. Un interno comparte una promo de su emprendimiento.",
    ], {
        "biz_topic": ["presupuesto anual", "reestructuración del equipo", "nueva herramienta CRM", "política de trabajo remoto", "evento corporativo", "evaluación de desempeño", "fusión con otra empresa", "lanzamiento de producto", "reducción de costos", "cambio de proveedor"],
    }
)

niche("job_interview", "Entrevistas de trabajo con situaciones realistas y respuestas humanas",
    "carrera", [
        "Escribe una entrevista laboral para {position} en {city}. El entrevistado: da una respuesta ensayada que se nota falsa, se traba en una pregunta simple, revela información no relevante sobre su vida personal, y hace una pregunta al final que muestra que no investigó la empresa. El entrevistador: sonríe profesionalmente mientras muere por dentro.",
        "Publicación en LinkedIn sobre {position} que alguien acaba de conseguir. Incluye: agradecimiento genérico a la empresa, mención a 'nuevos desafíos', una reflexión sobre su viaje profesional que oculta el privilegio, y tres hashtags. Comentarios: colegas felicitando y un reclutador no solicitado.",
        "Conversación de preparación para entrevista de {position} entre dos amigos. Practican respuestas pero se desvían: uno cuenta su peor entrevista, el otro da un consejo contradictorio, toman algo, y terminan viendo TikTok. Incluye nervios genuinos y apoyo genuino entre distracciones.",
        "Correo de rechazo para {position} seguido de la respuesta del candidato. El rechazo: genérico con una frase personalizada. La respuesta: agradece, pide feedback, insinúa que está sobrecalificado, y dice que 'siguió otros procesos'. El reclutador responde con un feedback ambiguo que no dice nada.",
        "Transcripción de una entrevista técnica para {position}. El entrevistado: resuelve el ejercicio pero lo explica mal, usa terminología incorrecta, se queda en blanco 10 segundos, y luego tiene una idea brillante. El entrevistador: da pistas, juzga en silencio, y decide que 'tiene potencial'. ",
    ], {
        "position": ["Desarrollador Full Stack", "Data Scientist", "Project Manager", "Diseñador UX/UI", "Analista de Marketing", "Gerente de Producto", "Community Manager", "Consultor SAP", "Ingeniero DevOps", "Scrum Master"],
        "city": ["Ciudad de México", "Bogotá", "Buenos Aires", "Santiago", "Lima", "Madrid", "Barcelona", "Medellín"],
    }
)

niche("journal_entry", "Entradas de diario personal con pensamientos genuinos y desordenados",
    "personal", [
        "Escribe la entrada de un diario de alguien que está procesando {life_event}. El texto: empieza con el clima o algo trivial, se desvía al evento principal, intercala recuerdos no relacionados, hace una pregunta retórica al universo, y termina con un plan vago para mañana. Escrito con frases incompletas y paréntesis.",
        "Diario de un día cualquiera. La persona escribe sobre {daily_struggle}. Alterna entre: quejarse, sentirse culpable por quejarse, encontrar algo bonito, y olvidar lo que iba a escribir. Menciona algo que le dijo un desconocido. Termina sin conclusión. Nota: un garabato mental.",
        "Entrada de diario después de una conversación importante sobre {life_event}. La persona: escribe lo que debería haber dicho, analiza en exceso lo que dijo el otro, se da cuenta de algo sobre sí mismo, y escribe un recordatorio de comprar algo mundano. El tono cambia de intenso a cotidiano abruptamente.",
        "Post en un diario anónimo en línea. Alguien escribe sobre {life_event} pero de forma encriptada, refiriéndose a personas y lugares con iniciales. Pide consejo pero no da suficiente contexto. Respuestas: gente que se proyecta, consejo contradictorio, y alguien que dice 'terapia'. ",
        "Diario de alguien con {daily_struggle} que intenta llevar un 'bullet journal' pero termina escribiendo párrafos gigantes. Una entrada: 'Lunes - hacer ejercicio ✔️ (caminé a la cocina). Hoy pensé en...' y se desvía en una reflexión de 3 párrafos. Incluye dibujos descritos.",
    ], {
        "life_event": ["una ruptura amorosa", "un cambio de ciudad", "la pérdida de un ser querido", "un logro importante", "una decepción", "un reencuentro", "una decisión difícil", "una crisis existencial"],
        "daily_struggle": ["la procrastinación", "la soledad", "la ansiedad social", "el síndrome del impostor", "el insomnio", "la insatisfacción laboral", "la presión familiar"],
    }
)

niche("cooking_recipe", "Recetas de cocina contadas como lo haría una persona real, no un chef",
    "cocina", [
        "Escribe una receta de {dish} como la contaría alguien que la aprendió de su {relative}. Incluye: medidas al ojo ('como un chorrito de aceite'), sustituciones herejes (si no tienes X, ponle Y), comentarios sobre la primera vez que la hicieron, y una advertencia dramática sobre un paso crítico. Errores de tipeo en temperaturas y tiempos.",
        "Reseña de una receta que salió mal. La persona intentó hacer {dish} pero: confundió un ingrediente, omitió un paso por leer rápido, improvisó un cambio que arruinó todo, y terminó pidiendo delivery. Culpa a la receta aunque fue su culpa. El tono es autocrítico y gracioso.",
        "Publicación en un grupo de Facebook de cocina: 'Alguien tiene una receta fácil de {dish}?'. Comentarios: una receta con 50 ingredientes, alguien que dice 'yo la hago sin tal cosa', un link a un video de YouTube mal grabado, y la OP que responde 'no tengo horno' después de 20 sugerencias.",
        "Receta familiar de {dish} transcrita de una videollamada con un {relative}. La receta es: imprecisa, llena de 'le pones así como hasta que se vea bien', incluye un ingrediente secreto que 'no le digas a nadie', y termina con 'y ya, fácil'. La persona que transcribe añade notas entre paréntesis.",
        "Thread en Twitter/X sobre cómo hacer {dish}. La persona escribe tips en tiempo real mientras cocina. Se olvida de un paso, lo añade después, quema algo, toma una foto que no se entiende, y al final dice 'quedó rico... creo'. Respuestas: recetas alternativas y un debate sobre ingredientes.",
    ], {
        "dish": ["paella valenciana", "tacos al pastor", "encebollado ecuatoriano", "arepas colombianas", "ceviche peruano", "milanesa napolitana", "chilaquiles verdes", "mole poblano", "causa limeña", "empanadas argentinas", "bandeja paisa", "curry tailandés"],
        "relative": ["abuela", "madre", "tía", "suegra", "vecina", "papá"],
    }
)

niche("travel_review", "Reseñas de viajes y experiencias turísticas auténticas",
    "viajes", [
        "Escribe la reseña de un viaje a {travel_dest}. El autor: idealizó el destino antes de ir, tuvo una experiencia mediocre, pero no quiere admitirlo completamente. Describe: el clima, una interacción con un local, la comida con comparaciones injustas, y concluye con un 'igual estuvo bonito' que esconde decepción.",
        "Post en un grupo de viajeros: 'Alguien ha ido a {travel_dest}?'. El OP pide recomendaciones. Recibe: 10 sugerencias de lugares, 5 advertencias exageradas de peligro, alguien que dice 'yo fui hace 10 años y era mejor', y un link a un blog con información desactualizada. El OP se abruma.",
        "Diario de viaje día 1 en {travel_dest}. La persona: perdió el vuelo, encontró el hostal en un callejón sospechoso, probó comida callejera y tuvo dudas existenciales, pero también vio un atardecer increíble. Escrito con emoción y agotamiento. Incluye un presupuesto en tiempo real que ya excedió.",
        "Reseña en TripAdvisor de un hotel en {travel_dest}. El huésped: se queja del ruido pero admite que el hotel no era ruidoso, solo que él tiene sueño ligero. Menciona que el desayuno 'estaba bien para ser gratis'. Incluye una foto mental del baño. Califica con 3 estrellas y texto de 4 párrafos.",
        "Conversación de WhatsApp con la familia durante un viaje a {travel_dest}. Alterna entre: fotos de comida, 'llegué bien', quejas del cambio climático, 'extraño mi cama', una selfie con un monumento de fondo, y un 'no sé dónde estamos pero está lindo'. La familia responde con emojis y encargos.",
    ], {
        "travel_dest": ["Cartagena de Indias", "Cusco", "Buenos Aires", "La Habana", "Barcelona", "Medellín", "Río de Janeiro", "Machu Picchu", "Tulum", "Galápagos", "Patagonia", "San Andrés", "Ciudad de Panamá", "Valparaíso"],
    }
)

niche("fitness_log", "Registros de ejercicio y hábitos con altibajos reales",
    "salud", [
        "Entrada de un diario de fitness. La persona: empezó el mes con gran motivación para {fitness_goal}, ya lleva 3 días saltándose el gym, justifica con excusas creativas, y escribe 'mañana sí' con menos convicción cada vez. Incluye: un momento de autocompasión y un recuento de lo que comió.",
        "Publicación en un grupo de fitness: 'Llevo {time} haciendo {fitness_goal} y no veo resultados'. Responde su propio post: 'actualización: ya medí mal'. Siguen comentarios: consejos no solicitados, alguien que dice 'genética', un coach vendiendo su programa, y alguien que comparte su transformación extrema.",
        "Post de Instagram transcrito sobre una rutina de {fitness_goal}. La persona: da instrucciones imprecisas, presume unintencionalmente, recomienda un suplemento caro, y revela que lleva solo 2 semanas entrenando. Escrito con lenguaje motivacional mezclado con realidades de principiante.",
        "Conversación entre dos personas en el gym sobre {fitness_goal}. Una da consejos con seguridad, la otra los sigue ciegamente. Descubren que ambos vieron el mismo video de YouTube. Terminan haciendo la mitad de la rutina y yendo a comer algo 'porque lo quemamos'. Incluye terminología mal usada.",
        "Bitácora de un corredor preparándose para una carrera. Entradas: día 1 - 'corrí 5k en 30 min, me siento increíble'. Día 2 - 'me duelen las rodillas'. Día 3 - 'vi un perro y caminé 20 min'. Día 4 - 'compré tenis nuevos'. Día de la carrera - 'llegué último pero terminé'.",
    ], {
        "fitness_goal": ["bajar de peso", "ganar masa muscular", "correr 10k", "hacer yoga diario", "ponerse en forma", "mejorar flexibilidad", "iniciar CrossFit", "natación recreativa"],
        "time": ["1 semana", "2 semanas", "un mes", "3 meses", "6 meses", "un año"],
    }
)

niche("real_estate", "Descripciones inmobiliarias y experiencias de búsqueda de vivienda",
    "vivienda", [
        "Escribe la descripción de un {property_type} en {city} como la escribiría un agente inmobiliario con poco filtro. Mezcla: frases hechas del rubro ('acogedor' = chico), detalles exagerados, verdades accidentales entre paréntesis, y una justificación del precio sin sentido. Incluye errores de ortografía en palabras técnicas.",
        "Un post en un grupo de alquileres: busco {property_type} en {city}. El OP: describe expectativas irreales con presupuesto irrisorio, añade requerimientos específicos que no negociará ('con estacionamiento para dos autos y balcón'), y responde a los comentarios defendiendo su presupuesto.",
        "Correo de un inquilino al propietario sobre problemas del {property_type}. Enumera 15 problemas, desde filtraciones hasta una toma de corriente chueca. El tono oscila entre cordial y amenazante sutilmente. Incluye una medición de humedad casera y fotos descritas. El propietario responde una semana después con 'y el horno?'.",
        "Comentario en redes: encontré {property_type} en {city} y el precio es sospechosamente bajo. Hilo de respuestas: 'seguro es estafa', 'yo fui a ver uno igual y era un departamento sin ventanas', 'con ese precio te compras algo mejor en otro lado', y el OP que actualiza 'era estafa, pedían depósito'.",
        "Descripción de una mudanza a un nuevo {property_type} en {city}. La persona: describe cada caja sin deshacer, la emoción del espacio vacío, el momento de pánico al ver la cocina, y una lista mental de muebles que necesita. El tono es de caos optimista. Menciona que el vecino se presentó con saludos incómodos.",
    ], {
        "property_type": ["departamento", "casa", "estudio", "loft", "casa de campo", "local comercial", "oficina", "terreno"],
        "city": ["Ciudad de México", "Buenos Aires", "Bogotá", "Medellín", "Lima", "Santiago", "Montevideo", "Quito", "Madrid"],
    }
)

niche("parenting_forum", "Conversaciones de crianza en foros y grupos con opiniones encontradas",
    "familia", [
        "Publicación en un grupo de madres/padres: 'Mi hijo de {age} años con {child_issue}, ¿alguien ha pasado por esto?'. Descripción larga con detalles no relevantes. Comentarios: consejos contradictorios (desde homeopatía hasta neuropediatra), alguien que juzga sin decir directamente, y un comentario empático que el OP nota.",
        "Escribe la respuesta de un pediatra en un consultorio virtual. El padre/madre describe {child_issue} con terminología sacada de Dr. Google y confianza peligrosa. El pediatra: corrige con cuidado, explica con ejemplos, y añade un consejo no médico al final ('y respire, papá'). Incluye interrupciones del niño de fondo.",
        "Experiencia de un primer día de escuela relatada en un grupo de WhatsApp familiar. El padre/madre narra cada detalle: la mochila, el llanto (de ambos), la maestra, el refrigerio. Incluye: fotos no solicitadas, actualizaciones cada hora, y una reflexión sobre el tiempo. Los familiares responden con emojis y anécdotas.",
        "Post en un foro anónimo: 'Estoy agotado como papá/mamá de {child_issue} y no sé si lo estoy haciendo bien'. Relato honesto sobre la dificultad de la crianza. Comentarios: apoyo genuino, 'es normal', y un 'te entiendo' que se siente más sincero que cualquier consejo.",
        "Diálogo en una reunión de padres de familia sobre organización del viaje de fin de curso. Una madre/padre quiere controlar todo, otro no opina, uno sugiere algo logísticamente imposible, y el delegado intenta mediar con un drive. Incluye: tensiones sutiles, chistes para aliviar, y pizza al final.",
    ], {
        "child_issue": ["problemas para dormir", "dificultades en el colegio", "pataletas frecuentes", "selectividad con la comida", "ansiedad por separación", "adaptación a hermanito", "uso excesivo de pantallas", "timidez extrema", "hiperactividad", "amistades conflictivas"],
        "age": list(range(1, 18)),
    }
)

niche("political_opinion", "Opiniones políticas expresadas en lenguaje cotidiano, no académico",
    "política", [
        "Escribe un comentario en redes sociales sobre {political_topic}. La persona: tiene una opinión firme pero la expresa con argumentos inconexos, menciona una noticia que vio a medias, y termina con una frase que contradice su punto inicial. Incluye mayúsculas para énfasis y etiquetas a cuentas que no leerán.",
        "Conversación familiar en una comida sobre {political_topic}. Dos {relative} discuten mientras otros intentan cambiar de tema. Incluye: referencias a 'en mis tiempos', una comparación con otro país que no es equivalente, alguien que saca un dato de memoria y todos lo aceptan, y un 'ya no se puede decir nada'.",
        "Post en un foro de discusión: 'Explicame {political_topic} como si tuviera 5 años'. Respuestas: una explicación simplista, una respuesta condescendiente, alguien que se queja de la analogía, y un link a un video de 3 horas. El OP pide más fuentes y el hilo se descarrila.",
        "Mensaje de voz transcrito a un amigo sobre {political_topic}. La persona: empieza hablando de otra cosa, se calienta gradualmente, usa mal un término técnico, menciona a un político como si lo conociera personalmente, y termina con 'bueno, después seguimos' sin conclusión.",
        "Carta al editor de un periódico local sobre {political_topic}. El autor: escribe con formalidad que se rompe en indignación genuina, incluye datos posiblemente incorrectos, una referencia a un evento local, y una sugerencia de solución que ignora la complejidad del problema. Firma con nombre y apellido y edad.",
    ], {
        "political_topic": ["la reforma de pensiones", "la seguridad ciudadana", "el sistema de salud público", "la inmigración", "los impuestos", "la educación pública", "el cambio climático", "la corrupción gubernamental", "el salario mínimo", "las políticas de género"],
        "relative": ["tíos", "hermanos", "primos", "papás", "abuelos", "cuñados"],
    }
)

niche("hobby_discussion", "Discusiones sobre hobbies y pasatiempos con jerga de entusiasta",
    "ocio", [
        "Un post en un foro de {hobby}: 'Soy nuevo, ¿por dónde empiezo?'. El OP no da contexto. Los miembros responden con: una guía para expertos, consejos contradictorios ('mejor empezá con X' vs 'no, mejor con Y'), un link a una wiki que abruma, y un 'bienvenido al vicio'. El OP no vuelve a aparecer.",
        "Escribe una reseña en una tienda especializada de {hobby} sobre un {product_hobby}. El reviewer: es dueño de 5 versiones anteriores, habla de especificaciones que solo entiende otro entusiasta, compara con el modelo del 98, y dice 'para empezar está bien' con elitismo apenas disimulado.",
        "Conversación de WhatsApp de un grupo de {hobby}. Una persona comparte su proyecto/logro reciente. Siguen: cumplidos genuinos, preguntas técnicas, alguien que comparte el suyo (uno-upmanship suave), y un meme interno. El grupo deriva a temas no relacionados y alguien retoma con 'volviendo al tema...'.",
        "Post en Instagram de un proyecto de {hobby} con descripción larga y emotiva. La persona: cuenta cómo empezó en el hobby, menciona que este proyecto le tomó X tiempo, agradece a otros miembros de la comunidad, y da tips. Los comentarios son: preguntas sobre materiales y 'está hermoso' repetido.",
        "Un miembro de un foro de {hobby} que abandona y vuelve después de 2 años: '¿siguen activos?'. Encuentra que: los mismos usuarios siguen activos, el equipo que usaba ya no se consigue, pero la comunidad sigue igual. Recibe un 'sí, acá seguimos, vos?' y retoma como si nada. Incluye actualización de su setup.",
    ], {
        "hobby": ["fotografía analógica", "juegos de mesa", "bicicletas de montaña", "acuarismo", "jardinería urbana", "cerveza artesanal", "instrumentos musicales", "modelismo", "ciclismo de ruta", "senderismo", "astronomía amateur", "cocina molecular", "cerámica", "cámping"],
        "product_hobby": ["cámara réflex", "bicicleta", "kit de acuario", "guitarra acústica", "telescopio", "tienda de campaña", "set de acuarela"],
    }
)

niche("restaurant_review", "Reseñas de restaurantes contadas como una experiencia completa",
    "gastronomía", [
        "Reseña de un restaurante en {city} donde la experiencia fue agridulce. El autor: describe el ambiente con poesía no intencional, la comida 'estaba bien', pero el servicio fue lento. Incluye: lo que pidió cada persona de su grupo, cuánto pagaron, y una comparación con otro restaurante que nadie pidió. Calificación: 4 estrellas con texto negativo.",
        "Reseña negativa pero mal escrita. El cliente: usa mayúsculas sin sentido, se queja de algo que no estaba en el menú, insulta al chef indirectamente, y amenaza con no volver. La gerencia responde con disculpa genérica y oferta de descuento. El cliente rechaza la oferta pero actualiza su reseña a 3 estrellas.",
        "Reseña de un restaurante nuevo en {city}. El autor: fue el día de la inauguración, todo salió mal (pedidos equivocados, tiempo de espera), pero lo perdona porque 'estaban empezando'. Describe los platos con detalles vívidos de alguien que claramente disfruta la comida. Recomienda volver en un mes.",
        "Un local recomienda su restaurante favorito de {city} en un hilo de Reddit. Escribe una reseña extensa con: historia del local, cómo descubrió el lugar, su pedido habitual, y una advertencia sobre el día de la semana que no hay el plato estrella. Defiende el lugar contra críticas menores con fiereza personal.",
        "Reseña de un restaurante caro en {city} escrita por alguien que fue por una ocasión especial. Incluye: expectativas altas, un plato que no justificaba el precio, otro que 'valió cada centavo', y una reflexión sobre si vale la pena. El autor admite que quizás no es su target pero agradece la experiencia.",
    ], {
        "city": ["Ciudad de México", "Buenos Aires", "Bogotá", "Lima", "Santiago", "Medellín", "Guadalajara", "Quito", "Caracas", "Montevideo", "La Paz", "Panamá"],
    }
)

niche("tech_tutorial", "Tutoriales técnicos explicados como lo haría un colega, no un manual",
    "tecnología", [
        "Escribe un tutorial sobre {tech_topic} como si un colega te lo explicara en el trabajo. El autor: asume que sabes algunas cosas (pero se equivoca en cuáles), se salta pasos 'obvios', los pasos que sí explica los complica, y añade comentarios como 'esto no sé por qué funciona pero no lo toques'. Incluye errores de tipeo en comandos.",
        "Post en un foro: 'Tutorial definitivo de {tech_topic}'. El autor promete un tutorial completo pero: se distrae explicando por qué eligió esa tecnología, incluye capturas del código que están borrosas, y al final pide donaciones. Los comentarios señalan errores y el OP no responde.",
        "Video tutorial transcrito de {tech_topic}. El creador: empieza con 'antes de empezar, suscríbete', explica algo mal, lo corrige después, olvida mostrar un paso importante, y termina con 'si les gustó den like'. La sección de comentarios tiene gente pidiendo ayuda con errores que el tutorial causó.",
        "Escribe una guía de {tech_topic} en un README de GitHub. El autor: mezcla español e inglés técnico, escribe las instrucciones para sí mismo del futuro más que para otros, incluye un ejemplo que no funciona porque falta un import, y tiene un FAQ de una sola pregunta que nadie ha hecho.",
        "Un hilo en Twitter/X donde alguien explica {tech_topic} en 20 tuits. Cada tuit: asume que leíste el anterior, tiene un error tipográfico en un comando crítico, y usa emojis de forma confusa. Alguien responde con el hilo corregido. El OP tuitea 'gracias por la corrección' sin editar el original.",
    ], {
        "tech_topic": ["desplegar una app en Railway", "conectar React con Firebase", "hacer scraping con Python", "crear un bot de Discord", "usar Docker por primera vez", "API REST con Node.js", "deploy con GitHub Actions", "testing con pytest", "manejo de estado en React", "autenticación JWT"],
    }
)

niche("personal_story", "Historias personales contadas como en una conversación con amigos",
    "personal", [
        "Escribe una historia personal graciosa sobre {life_moment}. El narrador: empieza contextualizando demasiado, da detalles irrelevantes, imita voces con descripciones entre paréntesis, y el clímax es anticlimático. El tono es de quien cuenta una anécdota en una cena con amigos. Incluye risas descritas y pausas dramáticas.",
        "Publicación en redes: 'Les voy a contar algo que me pasó...' sobre {life_moment}. Hilo de 10 tuits. Cada tuit: añade un detalle que cambia la historia, incluye un 'hilo 🧵' innecesario, y tiene una revelación que no es tan impactante como cree. Respuestas: 'jajaja', 'me pasó igual', y 'no te creo'.",
        "Historia contada en un subreddit de 'algo que me pasó y aún no lo supero' sobre {life_moment}. El OP: da contexto familiar completo, incluye diálogos reconstruidos (posiblemente ficcionados), y pide opinión. Comentarios: 'no eres el culpable', 'esto merece actualización', y 'nunca estuve tan enganchado a un post'.",
        "Anécdota contada en un ascensor (transcrita por un testigo). Dos desconocidos: uno cuenta {life_moment} al otro mientras suben 10 pisos. El que escucha: hace preguntas, ofrece su propia anécdota más corta, y se bajan juntos sin intercambiar nombres. La historia incluye interjecciones y lenguaje corporal descrito.",
        "Carta a un amigo por correo electrónico contando {life_moment}. El autor: justifica por qué no ha escrito en meses, da una actualización de su vida en desorden cronológico, y la historia principal se pierde en detalles. Termina con 'te cuento más cuando hablemos' y un chiste interno.",
    ], {
        "life_moment": ["la peor cita de mi vida", "un viaje que salió mal", "una entrevista desastrosa", "el día que conocí a mi mejor amigo", "cuando me equivoqué de avión", "una mudanza catastrófica", "el evento más random que presencié", "cuando conocí a un famoso sin querer"],
    }
)

niche("product_comparison", "Comparativas de productos escritas como recomendación de amigo",
    "opiniones", [
        "Escribe una comparativa entre {product_a} y {product_b} como si se la explicaras a un amigo. El autor: favores uno sin razón técnica, menciona una característica de {product_b} que no entendió bien, y recomienda el que él tiene. Incluye: una historia de su experiencia personal y un 'en resumen' que contradice el texto.",
        "Post en un foro: 'Ayuda, no sé si comprar {product_a} o {product_b}'. El OP lista sus necesidades pero ninguna es específica. Respuestas: mitad recomienda A, mitad B, un 'depende', y alguien que sugiere un producto C que nadie mencionó. El OP actualiza: 'compré A' sin explicación.",
        "Video de YouTube transcrito: comparativa {product_a} vs {product_b}. El creador: empezó objetivo pero ya tiene favorito, usa términos de marketing como 'revolucionario' para cosas básicas, y el 'veredicto final' es ambiguo. Incluye: una anécdota de uso, un error factual en especificaciones, y un 'link en descripción' para ambos.",
        "Reseña comparativa en Amazon: compré {product_a} y {product_b} para decidir cuál quedar. Descripción detallada: desempaquetado (importante), primeras impresiones, uso durante una semana, y un momento de 'revelación' con uno. El reviewer devolvió el otro. Fotos descritas: una con mala iluminación.",
        "Conversación en un grupo de tecnología: alguien pregunta {product_a} o {product_b}. Se arma un debate de 100 mensajes con: fanboys de cada marca, análisis técnicos que nadie entiende, ofertas de otros modelos, y un 'cómprate el que más te guste' que cierra el tema. El OP nunca confirma qué compró.",
    ], {
        "product_a": ["PlayStation 5", "iPhone 16", "MacBook Air M3", "Samsung Galaxy S25", "AirPods Pro", "Kindle Paperwhite", "Nintendo Switch 2", "Dyson V15", "Sonos Era 100"],
        "product_b": ["Xbox Series X", "Google Pixel 10", "Dell XPS 17", "iPhone 16 Pro", "Sony WH-1000XM5", "Tablet Samsung", "Steam Deck", "Roborock S8", "JBL Charge 5"],
    }
)

niche("career_advice", "Consejos profesionales y discusiones sobre crecimiento laboral",
    "carrera", [
        "Un post en LinkedIn: 'Después de {years} años en {industry}, he decidido...' sobre un cambio profesional. El post: reflexivo, inspirador, con un toque de privilegio no reconocido. Comentarios: 'felicidades', 'me inspiras', 'te mandé mensaje', y un reclutador ofreciendo algo no relacionado.",
        "Hilo en un foro de carreras: 'Tengo {age} años y no sé qué hacer con mi vida'. El OP describe su situación con detalles. Respuestas: gente que le dice que está joven, reconversión profesional, cursos online, y alguien que comparte su historia de éxito. El OP sigue confundido pero agradece.",
        "Escribe una sesión de mentoría sobre {career_topic}. El mentoreado: llega con una lista de preguntas desorganizadas, interrumpe al mentor con 'pero es que...', y revela que no ha hecho la tarea de la sesión anterior. El mentor: paciente pero firme, da ejemplos de su carrera, y termina con un plan de acción.",
        "Conversación en la hora del almuerzo en una oficina sobre {career_topic}. Cinco colegas discuten: unos quieren crecer en la empresa, otros irse a startup, uno está conforme. Incluye: quejas del jefe, estimaciones salariales incorrectas, chisme corporativo, y un 'yo también estoy viendo opciones' susurrado.",
        "Post en Reddit CareerAdvice: '¿Debo aceptar esta oferta? sobre {career_topic}. El OP detalla: salario actual vs oferta, beneficios, cultura, commute. Comentarios: 'negocia', 'no aceptes la primera oferta', 'el dinero no lo es todo', y 'yo estuve en esa empresa y es horrible'. El OP actualiza: 'acepté'.",
    ], {
        "career_topic": ["cambio de industria", "negociación salarial", "ascenso vs equilibrio vida-trabajo", "emprender vs empleado", "estudiar un posgrado", "trabajo remoto vs presencial", "cómo pedir un aumento", "burnout laboral", "desarrollo de habilidades blandas", "cómo renunciar profesionalmente"],
        "years": [5, 8, 10, 12, 15, 20],
        "age": [22, 25, 28, 30, 35, 40, 45],
        "industry": ["tecnología", "marketing", "finanzas", "consultoría", "educación", "salud", "recursos humanos", "ventas"],
    }
)

niche("movie_review", "Reseñas de películas/series con opiniones de espectador común",
    "entretenimiento", [
        "Reseña de {movie} en Letterboxd escrita por alguien que no es crítico. El autor: admite que no entendió partes, la compara con otra película solo porque tienen el mismo actor, y su mayor crítica es sobre la duración. Incluye: una referencia a lo que comió durante la película y una calificación de 3.5 estrellas con texto emotivo.",
        "Conversación de amigos saliendo del cine después de ver {movie}. Discuten: si les gustó o no, un plot hole que 'descubrieron', la banda sonora, y quién actuó mejor. Uno defiende la película con argumentos débiles, otro la critica sin haberla entendido del todo. Terminan yendo a cenar y cambian de tema.",
        "Hilo en Twitter/X sobre {movie}: la persona tuitea en vivo durante la película. Comentarios: confusión sobre personajes, predicciones erradas, quejas de otros espectadores imaginarios, y un 'ya se acabó??' al final. El hilo tiene más engagement que la crítica profesional.",
        "Post en Facebook: 'Alguien más vio {movie}?'. Texto largo con: resumen inexacto de la trama, opinión sobre el final sin spoiler warnings, y una pregunta a los amigos. Comentarios: gente que la amó, gente que la odió, y uno que dice 'no la he visto pero leí el libro y es mejor'.",
        "Reseña en IMDB de {movie} con 1 estrella porque 'no le entendí' o con 10 estrellas porque 'es la mejor película de la historia'. Texto corto, escrito emocionalmente, con errores gramaticales y una queja o alabanza muy específica que delata que el reviewer no vio la película completa.",
    ], {
        "movie": ["Dune: Part Two", "Oppenheimer", "Inside Out 2", "Barbie", "The Batman", "Everything Everywhere All At Once", "Poor Things", "The Zone of Interest", "Past Lives", "Across the Spider-Verse"],
    }
)

niche("book_club", "Conversaciones de un club de lectura con opiniones diversas",
    "lectura", [
        "Un post en un club de lectura sobre {book}. El miembro: empezó el libro con entusiasmo, luego se estancó, y terminó con opiniones encontradas. Describe su relación con los personajes como si fueran personas reales. Incluye: comparaciones con el autor anterior, una confesión de que saltó páginas, y una calificación ambigua.",
        "Conversación de WhatsApp de un club de lectura discutiendo {book}. Miembros: uno amó el libro con pasión, otro lo odió con argumentos, uno no lo terminó pero opina igual, y el coordinador intenta mantener el orden. Incluye: spoilers sin avisar, debates que se desvían a política, y emojis de libros.",
        "Reseña en Goodreads de {book} de alguien que lee 100 libros al año. Crítica: estructurada pero con opiniones fuertes, mención a la traducción si es relevante, una cita favorita, y una comparación con otro libro del mismo género. Puntuación: 3 estrellas con texto de 5 estrellas o viceversa.",
        "Un hilo en BookTok transcrito: recomendación de {book} con exclamaciones excesivas. La persona: resume el libro mal pero vende la experiencia, muestra el libro con stickers, menciona que 'lloró', y etiqueta al autor. Comentarios: 'lo añado a mi TBR', 'ese libro me cambió la vida', y 'no me gustó'.",
        "Correo de una bibliotecaria/reseñadora recomendando {book}. Escribe con: análisis literario genuino mezclado con reacciones personales, una advertencia sobre contenido sensible, un spoiler marcado que revela demasiado, y una invitación a discutir. Tono entre académico y entusiasta.",
    ], {
        "book": ["Cien Años de Soledad - Gabriel García Márquez", "La Sombra del Viento - Carlos Ruiz Zafón", "2666 - Roberto Bolaño", "Los Detectives Salvajes - Roberto Bolaño", "La Casa de los Espíritus - Isabel Allende", "Rayuela - Julio Cortázar", "El Amor en los Tiempos del Cólera - Gabriel García Márquez", "La Tregua - Mario Benedetti", "Pedro Páramo - Juan Rulfo", "La Ciudad y los Perros - Mario Vargas Llosa"],
    }
)

niche("gaming_community", "Conversaciones de comunidades de videojuegos",
    "videojuegos", [
        "Un post en un foro de {game}: discusión sobre la mejor build/clase/estrategia. El OP propone una build poco óptima pero divertida. Respuestas: min-maxers que optimizan la diversión, alguien que comparte su build rota, y un veterano que dice 'en la versión 1.0 esto era mejor'. El OP defiende su build con pasión.",
        "Escribe una reseña de {game} en Steam con horas de juego. El reviewer: tiene 500+ horas y la reseña dice 'No recomiendo este juego'. Explica con detalles de mecánicas, menciona una actualización que lo arruinó, y termina diciendo 'pero no puedo dejar de jugarlo'. Incluye una captura de un bug gracioso.",
        "Transcripción de una partida online de {game}. Cuatro jugadores: uno lleva al equipo, otro no sabe qué hace, uno hace roleplay sin que nadie le siga, y el cuarto está en mute. Incluye: momentos de tensión, risas, insultos amistosos, y un 'gg' al final. Terminan agregándose como amigos.",
        "Hilo en Reddit: '{game} me salvó la vida' o similar. El OP comparte una historia personal emocional sobre cómo {game} le ayudó en un momento difícil. Comentarios: apoyo, historias similares, y un 'a mí también me pasó'. Un comentario fuera de lugar preguntando specs de PC.",
        "Discusión en Discord de {game}: se anunció una actualización/DLC y el canal explota. Miembros: especulan sobre contenido, comparan con juegos similares, hacen memes, organizan partidas para celebrar, y alguien se queja del precio. El admin pone un rol de 'emocionados' y el caos reina.",
    ], {
        "game": ["Elden Ring", "Baldur's Gate 3", "Zelda: Tears of the Kingdom", "Stardew Valley", "Valorant", "Counter-Strike 2", "World of Warcraft", "Minecraft", "Fortnite", "Final Fantasy VII Rebirth", "Helldivers 2", "Palworld", "Cyberpunk 2077", "Red Dead Redemption 2"],
    }
)

niche("pet_care", "Conversaciones sobre mascotas con dueños apasionados y preocupados",
    "mascotas", [
        "Publicación en un grupo de Facebook de mascotas: 'A mi {pet_type} le pasa esto...' describiendo un síntoma que el dueño googleó y ahora está convencido de que es grave. Incluye: fotos no muy claras del animal, una descripción de su personalidad como si fuera humano, y 'alguien ha pasado por esto?'.",
        "Escribe la conversación en la sala de espera del veterinario. Varios dueños: uno con {pet_type} que está ahí por {pet_issue}, otro con una mascota saludable solo por control, y un tercero que habla de su mascota fallecida con nostalgia. Comparten historias, consejos no solicitados, y fotos. La tensión baja cuando sale el veterinario.",
        "Un hilo en Reddit sobre {pet_issue} con {pet_type}. El OP describe el problema con detalles médicos que claramente copió de Google. Respuestas: 'llevalo al vet ya', 'a mi mascota le pasó y era...', 'prueba con esto (consejo peligroso)', y un veterinario real que aparece y corrige a todos.",
        "Escribe la actualización de Instagram de alguien que acaba de adoptar un {pet_type}. Día 1: 'miren lo que llegó a la familia 🥹'. Día 2: 'ya rompió mis zapatos'. Día 3: 'lo amo pero no puedo dormir'. Día 7: 'es parte de la familia'. Cada post tiene fotos del animal en poses cada vez más dueñas de la casa.",
        "Diálogo entre dos dueños en un parque de perros mientras sus mascotas juegan. Tema: {pet_issue}. Uno da consejos con seguridad ('a mi perro le pasó y le di X'), el otro escucha cortésmente pero no piensa seguirlos. Incluye: perros que se enredan en las correas, un encuentro tenso que termina en colas moviéndose, y planes para repetir.",
    ], {
        "pet_type": ["perro (labrador)", "gato (común europeo)", "perro (rescate)", "hámster", "conejo", "perro (chihuahua)", "gato (persa)", "loro", "tortuga", "pez betta"],
        "pet_issue": ["vómitos frecuentes", "pérdida de apetito", "ansiedad por separación", "problemas de piel", "sobrepeso", "agresividad con otros animales", "no usa la caja de arena", "ladridos excesivos", "muda excesiva de pelo", "problemas dentales"],
    }
)

niche("home_improvement", "Proyectos de bricolaje y mejoras del hogar con resultados mixtos",
    "hogar", [
        "Un post en un foro de bricolaje: 'Quiero hacer {project} pero no tengo experiencia'. El OP describe su plan con optimismo y pide consejo. Respuestas: 'es más difícil de lo que crees', 'yo lo hice y me quedó bien (foto borrosa)', 'contrata a un profesional', y 'dale para adelante, yo confío en vos'. El OP hace el proyecto y actualiza: 'no salió como esperaba'.",
        "Escribe una guía de {project} en un blog personal. El autor: empezó emocionado, encontró problemas que no anticipó, improvisó soluciones cuestionables, y el resultado final es 'funcional pero no bonito'. Incluye: fotos de cada paso donde el área de trabajo se vuelve más caótica, y un resumen de costos que duplica el presupuesto inicial.",
        "Conversación en una ferretería: cliente busca materiales para {project}. El vendedor recomienda algo incorrecto, el cliente confía, y otro cliente interviene corrigiendo. Terminan los tres discutiendo el proyecto, y el vendedor terminará comprando los materiales correctos. Incluye: terminología mal usada por todos.",
        "Post en Instagram de un antes/después de {project}. La persona: describe el proceso con entusiasmo y hashtags de decoración. Lo que no muestra: las 3 veces que casi se rinde, los muebles que dañó, y el presupuesto que voló. Sin embargo, el resultado se ve bien en la foto. Comentarios: '¿me haces el mío?' y 'dónde compraste?'.",
        "Relato de una pareja haciendo {project} juntos. Ella: quiere que quede perfecto, lee las instrucciones completas. Él: quiere 'tirar para adelante', no lee nada. Incluye: un momento en que algo se rompe, la culpa mutua, la reconciliación, y cerveza de por medio. El proyecto se termina 3 fines de semana después de lo planeado.",
    ], {
        "project": ["pintar una habitación", "armar un mueble de IKEA", "cambiar el piso de la cocina", "instalar una estantería flotante", "reparar una gotera", "construir un jardín vertical", "cambiar la cerradura", "instalar un termo eléctrico", "hacer una mesa de madera", "cablear una oficina en casa"],
    }
)


NICHE_CATEGORIES = {}
for n, info in NICHES.items():
    cat = info["category"]
    if cat not in NICHE_CATEGORIES:
        NICHE_CATEGORIES[cat] = []
    NICHE_CATEGORIES[cat].append(n)

NICHE_KEYS = list(NICHES.keys())
