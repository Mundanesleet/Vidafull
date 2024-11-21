document.addEventListener('DOMContentLoaded', function () {

    

    // Inicializar Flatpickr en el campo de texto con el id 'fecha'
    flatpickr("#fecha", {
        dateFormat: "Y-m-d", // Formato de la fecha
        locale: "es", // Establecer idioma en español (opcional)
        onChange: function (selectedDates) {
            // Cuando se seleccione una fecha, actualizamos el calendario de abajo
            let selectedDate = selectedDates[0]; // Solo tomamos la primera fecha seleccionada

            // Actualizar el calendario en el div #calendario con la fecha seleccionada
            calendario.gotoDate(selectedDate); // Mueve el calendario a la fecha seleccionada

            // Resaltar la fecha seleccionada en FullCalendar
            const selectedDateStr = selectedDate.toISOString().split('T')[0]; // Formato "Y-m-d"
            
            // Marcar la celda del calendario
            const selectedDayCell = document.querySelector(`[data-date="${selectedDateStr}"]`);
            if (selectedDayCell) {
                selectedDayCell.classList.add('selected'); // Asegúrate de que esta clase esté definida en tu CSS
            }
        }

    });

    const buttons = document.querySelectorAll('.custom-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Alterna la clase 'hora-seleccionada' solo en el botón que fue clicado
            button.classList.toggle('hora-seleccionada');
        });
    });


    const selectedDates = []; // Inicializar el array de fechas seleccionadas
    const today = new Date(); // Obtener la fecha actual

    let calendario = new FullCalendar.Calendar(document.getElementById('calendario'), {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: { left: 'prev', center: 'title', right: 'next' },
        titleFormat: { month: 'long' },
        dateClick: info => {
            const clickedDate = new Date(info.date);
            const localDateStr = clickedDate.toISOString().split('T')[0];

            if (selectedDates.includes(localDateStr)) {
                selectedDates.splice(selectedDates.indexOf(localDateStr), 1);
                info.dayEl.classList.remove('selected');
            } else {
                selectedDates.push(localDateStr);
                info.dayEl.classList.add('selected');
            }

            updateSelectedDatesDisplay();
        },

        events: [], // Sin eventos predefinidos
        eventColor: '#378006',
        dayCellDidMount: info => {
            // Marcar días seleccionados
            if (selectedDates.includes(info.dateStr)) {
                info.el.classList.add('selected'); // Agregar la clase de estilo
            }

            // Obtener el número del día directamente desde info.date
            const dayNumber = info.date.getDate(); // Obtener el día del mes (1-31)

            // Formatear el día para que tenga un 0 delante si es menor que 10
            const formattedDayNumber = dayNumber < 10 ? `0${dayNumber}` : dayNumber;

            // Cambiar el texto del día en el elemento correspondiente solo si está vacío
            if (!info.el.innerText) {
                info.el.innerText = formattedDayNumber; // Cambiar el texto del día a solo el número formateado
            }
        }
    });


    calendario.render();
    calendario.gotoDate(today); // Establecer la fecha predeterminada en el calendario

    const updateSelectedDatesDisplay = () => {
        const selectedDatesContainer = document.getElementById('selectedDates');

        // Mostrar el día actual al cargar la página
        const currentDay = new Date();
        const options = { weekday: 'long', day: 'numeric' };
        const formattedCurrentDay = currentDay.toLocaleDateString('es-ES', options);
        const capitalizedCurrentDay = formattedCurrentDay.charAt(0).toUpperCase() + formattedCurrentDay.slice(1);

        // Si no hay fechas seleccionadas, mostrar el día actual
        if (selectedDates.length === 0) {
            selectedDatesContainer.innerText = capitalizedCurrentDay;
            return;
        }

        // Ordenar las fechas seleccionadas
        selectedDates.sort((a, b) => new Date(a) - new Date(b));

        // Obtener la menor y mayor fecha
        const start = new Date(selectedDates[0]);
        const end = new Date(selectedDates[selectedDates.length - 1]);

        // Ajustar las fechas para eliminar el desfase de un día en función de la zona horaria local
        const localStart = new Date(start.getUTCFullYear(), start.getUTCMonth(), start.getUTCDate());
        const localEnd = new Date(end.getUTCFullYear(), end.getUTCMonth(), end.getUTCDate());

        // Obtener el día y el número de la fecha
        const options1 = { weekday: 'long', day: 'numeric' };
        const startFormatted = localStart.toLocaleDateString('es-ES', options1).replace(/^./, c => c.toUpperCase());
        const endFormatted = localEnd.toLocaleDateString('es-ES', options1).replace(/^./, c => c.toUpperCase());

        // Mostrar las fechas seleccionadas
        selectedDatesContainer.innerText =
            selectedDates.length === 1 ? startFormatted : `${startFormatted} - ${endFormatted}`;
    };

    // Llamar a la función para mostrar el día actual al cargar la página
    updateSelectedDatesDisplay();
});