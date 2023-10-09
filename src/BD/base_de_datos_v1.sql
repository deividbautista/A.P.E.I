-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-10-2023 a las 22:29:38
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `base_de_datos_v1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignaciones`
--

CREATE TABLE `asignaciones` (
  `Id_asignaciones` int(11) NOT NULL,
  `id_usuarios` int(11) DEFAULT NULL,
  `id_proceso` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asignaciones`
--

INSERT INTO `asignaciones` (`Id_asignaciones`, `id_usuarios`, `id_proceso`) VALUES
(88, 1, 574281936);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `procesos`
--

CREATE TABLE `procesos` (
  `id_proceso` int(11) NOT NULL,
  `Titulo` varchar(60) NOT NULL,
  `Descripcion` longtext DEFAULT NULL,
  `Fecha_inicio` date DEFAULT NULL,
  `Fecha_terminación` date DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `ReporteGenerado` varchar(15) NOT NULL,
  `Estado_proceso` int(2) NOT NULL,
  `Nivel_importancia` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `procesos`
--

INSERT INTO `procesos` (`id_proceso`, `Titulo`, `Descripcion`, `Fecha_inicio`, `Fecha_terminación`, `fecha_creacion`, `ReporteGenerado`, `Estado_proceso`, `Nivel_importancia`) VALUES
(574281936, 'Entrega de suministros', 'En el contexto de la frase \"I’m the antonymph of the internet\" que mencionaste anteriormente, podemos inferir que la artista vylet pony está utilizando el término \"antonymph\" para expresar que ella representa lo opuesto o contrastante con el mundo de internet.  Dado que la ninfa se asocia con la vitalidad y la belleza de la naturaleza, podemos interpretar que la artista está sugiriendo que ella es una fuerza opuesta a la artificialidad, la inautenticidad o los aspectos negativos que pueden estar presentes en el mundo en línea.  La frase \"Still cleaning up the viruses that you had left\" puede indicar que la artista está asumiendo el papel de limpiar y contrarrestar los efectos negativos dejados por otros en el entorno digital. Podría referirse a la idea de eliminar los aspectos tóxicos, los engaños o los problemas que pueden surgir en el mundo de internet.  En resumen, la frase \"I’m the antonymph of the internet\" en este contexto parece transmitir la idea de que la artista vylet pony se considera a sí misma.\r\n                            \r\n                            \r\n                            \r\n                            \r\n                            ', '2023-09-26', '2023-10-03', '2023-09-26 14:05:02', '', 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuarios` int(11) NOT NULL,
  `NDI` int(20) NOT NULL,
  `Contraseña` char(102) NOT NULL,
  `Nombre_completo` varchar(50) NOT NULL,
  `Direccion` varchar(30) NOT NULL,
  `Telefono` int(15) NOT NULL,
  `Empresa` varchar(35) NOT NULL,
  `Cargo` varchar(25) NOT NULL,
  `Area_locativa` varchar(30) NOT NULL,
  `Email` varchar(35) NOT NULL,
  `Fecha_nacimiento` date DEFAULT NULL,
  `Rol` tinyint(1) NOT NULL,
  `Nombre_img` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores the user''s data.';

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuarios`, `NDI`, `Contraseña`, `Nombre_completo`, `Direccion`, `Telefono`, `Empresa`, `Cargo`, `Area_locativa`, `Email`, `Fecha_nacimiento`, `Rol`, `Nombre_img`) VALUES
(1, 1010166424, 'pbkdf2:sha256:600000$PKyNFkIhaLNxRkg3$eef35b3a10abd6667d3edac1e3b759ae55052b2344cc3a40e7b7b1bffc1a3618', 'Deivid Edwuar Bautista Ocampo.', 'calle siempre viva109', 31212287, 'Americana de servicios L.T.D.A', 'Aprendiz', 'Oficina', 'debautist15@gmail.com', '2023-05-02', 0, '1010166424.jpg');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asignaciones`
--
ALTER TABLE `asignaciones`
  ADD PRIMARY KEY (`Id_asignaciones`),
  ADD KEY `fk_asignaciones_users` (`id_usuarios`),
  ADD KEY `id_proceso` (`id_proceso`);

--
-- Indices de la tabla `procesos`
--
ALTER TABLE `procesos`
  ADD PRIMARY KEY (`id_proceso`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asignaciones`
--
ALTER TABLE `asignaciones`
  MODIFY `Id_asignaciones` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT de la tabla `procesos`
--
ALTER TABLE `procesos`
  MODIFY `id_proceso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2147483648;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asignaciones`
--
ALTER TABLE `asignaciones`
  ADD CONSTRAINT `asignaciones_ibfk_1` FOREIGN KEY (`id_proceso`) REFERENCES `procesos` (`id_proceso`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_asignaciones_users` FOREIGN KEY (`id_usuarios`) REFERENCES `usuarios` (`id_usuarios`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
