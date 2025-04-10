import React from "react";

const DivisionIncorrectaSVG = ({ dividendo, divisor, respuestaCorrecta, respuestaUsuario }) => {
  const cajaWidth = 300 / divisor; // Ancho de cada caja
  const cajaHeight = 60; // Altura de cada caja
  const bolaRadius = 8; // Tamaño de las bolas
  const maxBolasPorFila = Math.floor(cajaWidth / (bolaRadius * 2)); // Cantidad de bolas por fila
  const margenIzquierdo = 55; // 🔹 Se ajusta la posición inicial más cerca del borde izquierdo

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginBottom: "20px" }}>
      <h3>Visualización de la división incorrecta</h3>

      <svg width="400" height="300" viewBox="0 0 400 300">
        {/* Etiquetas */}
        <text x="20" y="30" fontSize="10" fontWeight="bold" fill="green">✅ Correcto:</text>
        <text x="20" y="170" fontSize="10" fontWeight="bold" fill="red">❌ Tu respuesta:</text>

        {/* Cajas correctas arriba */}
        {[...Array(divisor)].map((_, i) => (
          <rect key={`correct-box-${i}`} x={margenIzquierdo + i * cajaWidth} y={40} width={cajaWidth} height={cajaHeight} fill="none" stroke="black" strokeWidth="2" />
        ))}

        {/* Cajas incorrectas abajo */}
        {[...Array(divisor)].map((_, i) => (
          <rect key={`user-box-${i}`} x={margenIzquierdo + i * cajaWidth} y={180} width={cajaWidth} height={cajaHeight} fill="none" stroke="black" strokeWidth="2" />
        ))}

        {/* Bolas correctas (más alineadas a la izquierda) */}
        {[...Array(respuestaCorrecta * divisor)].map((_, i) => {
          const cajaIndex = Math.floor(i / respuestaCorrecta);
          const filaIndex = Math.floor((i % respuestaCorrecta) / maxBolasPorFila);
          const columnaIndex = (i % respuestaCorrecta) % maxBolasPorFila;

          return (
            <circle
              key={`correct-${i}`}
              cx={margenIzquierdo + cajaIndex * cajaWidth + columnaIndex * bolaRadius * 2 + bolaRadius} 
              cy={50 + filaIndex * bolaRadius * 2}
              r={bolaRadius}
              fill="green"
            />
          );
        })}

        {/* Bolas incorrectas (más alineadas a la izquierda) */}
        {[...Array(respuestaUsuario * divisor)].map((_, i) => {
          const cajaIndex = Math.floor(i / respuestaUsuario);
          const filaIndex = Math.floor((i % respuestaUsuario) / maxBolasPorFila);
          const columnaIndex = (i % respuestaUsuario) % maxBolasPorFila;

          return (
            <circle
              key={`user-${i}`}
              cx={margenIzquierdo + cajaIndex * cajaWidth + columnaIndex * bolaRadius * 2 + bolaRadius} 
              cy={190 + filaIndex * bolaRadius * 2}
              r={bolaRadius}
              fill="red"
            />
          );
        })}
      </svg>

      <p>
        <strong>✅ Correcto:</strong> {dividendo} ÷ {divisor} = {respuestaCorrecta}
      </p>
      <p>
        <strong>❌ Tu respuesta:</strong> {respuestaUsuario}
      </p>
    </div>
  );
};

export default DivisionIncorrectaSVG;
