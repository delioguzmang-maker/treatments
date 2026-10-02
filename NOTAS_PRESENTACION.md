# Notas para la presentación: crash criteria v8

Archivo: `SCDOT_AASHTOWare_Safety_Treatments_and_Countermeasures_v8.xlsx`
Base: el archivo que mandaste (4 hojas). Mismo orden de las 30 countermeasures, mismos 133 treatments.

---

## 1. El problema de fondo, en una frase

Las crash criteria estaban escritas con los campos y códigos del **TR-310 nuevo (MMUCC)**, pero el SMS y AASHTOWare Safety en producción usan el **diccionario viejo de SC**. Los nombres de campo no existen y varios códigos significan otra cosa.

Lo confirmé con el diccionario de datos de SC (SCDPS, 6/2010), que coincide con los códigos que viste en el SMS (13 = NON-JUNCTION, 56 = Median Barrier, 60 = Tree, etc.).

| La hoja decía | En el SMS ese código es | El correcto en el SMS |
|---|---|---|
| Pedestrian (26) | **Pedalcycle** | Pedestrian = 27 |
| Pedalcycle (25) | Motor Vehicle (Parked) | Pedalcycle = 26 |
| Angle (80) | no existe | Angle = 41, 42, 43 |
| Tree 57 | Overhead Sign Support | Tree = 60 |
| Utility Pole 59 | Other (Wall, Bldg, Tunnel) | Utility Pole = 61 |
| Guardrail 41 | Bridge Parapet End | Guardrail End 50 / Face 51 |
| Median Barrier 44 | Culvert | Median Barrier = 56 |
| Curve Left (02) / Right (03) | campo no existe | Road Character = Curve-Level / On Grade / Hillcrest |
| Dark-Lighted (05) | Dark (Street Lamp Lit) sí, pero 04 y 06 están corridos | Light 4-7 |
| Relation to Junction = Non-Junction (00) | campo no existe | Junction Type = NON-JUNCTION |

**Qué se hizo:** las 30 criteria se reescribieron con los nombres de campo y las etiquetas del dropdown, una línea por fila del Condition Builder, con los paréntesis marcados. Los códigos solo quedan en la hoja *Field Reference*, para revisar el JSON.

Además: según la reunión, los reportes del formulario nuevo **todavía no se cargan en producción** ("we cannot import JSONs in production right now"). O sea, hoy todo lo que se consulta está en el formato viejo. Cuando se carguen, en MMUCC "Ran off Road" y "Cross Median" dejan de ser harmful events y solo quedan en Sequence of Events. Está anotado en Field Reference, regla 5.

---

## 2. Tres trampas del Condition Builder (Field Reference, abajo)

1. **Paréntesis.** `A AND B OR C` se lee `(A AND B) OR C`. En tu query de median barriers, sin agrupar, el `AADT > 20000` y el `NON-JUNCTION` solo aplican a una parte de los ORs. En el builder hay que meter los ORs en un grupo.
2. **Exclusiones con AND, no OR.** `X ≠ a OR X ≠ b` siempre es verdadero.
3. **`≠` en campos de unidad** (Sequence of Events, Probable Cause, Unit Type, maniobra) solo quita esa fila, no el choque. Solo usar `≠` en campos de choque. Excepción práctica: en Roadway Departure hay una sola unidad, así que `Probable Cause ≠ Obstruction in Roadway` sí funciona ahí.

---

## 3. Median Barriers: cómo quedó y por qué

```
Junction Type = NON-JUNCTION
AND Trafficway = Two-Way, Divided, Unprotected Median
AND AADT > 20000
AND (   Manner of Collision = Head On
     OR Manner of Collision = Sideswipe, Opposite Direction
     OR Sequence of Events = Cross Median/Center
     OR Sequence of Events = Ran off Road Left
     OR First Harmful Event Location = Median )
AND First Harmful Event Location ≠ Roadside
AND First Harmful Event Location ≠ Outside Trafficway
AND Crash Harmful Event ≠ Median Barrier
```

- **Trafficway = Divided, Unprotected Median**: saca vías sin dividir (eso es centerline), rampas one-way y vías que ya tienen barrera.
- **First Harmful Event Location = Median**: con una línea entran todos los objetos en la mediana (pilares, estribos, muros, postes, cunetas, terraplenes, árboles). Era lo que faltaba.
- **AADT > 20,000**: coincide con AASHTO Roadside Design Guide, Fig. 6-1.
- **Cambié** tu `First Harmful Event ≠ Ran off Road Right` por `Location ≠ Roadside`. Razón: el que se sale a la derecha, sobrecorrige y cruza la mediana es justo el choque que la barrera evita, y tu condición lo sacaba. `Roadside` en una vía dividida es el lado de afuera, así que saca lo mismo sin perder ese caso.
- Uso **Sequence of Events** con `=` (inclusión). Eso sí funciona aunque sea campo multi-fila.

Prueba con los choques que ya revisaste:

| Choque | Qué pasó | Resultado | Por qué |
|---|---|---|---|
| 23206503 (I-26) | U1 se salió a la derecha → cerca → carro estacionado; MOC dice Head On | Fuera* | Primer harmful event (la cerca) en Roadside |
| 23210041 (I-26) | Se salió a la izquierda → volcó en la mediana | Dentro | Location = Median |
| 23239996 (I-20) | Mismo sentido, cambio de carril; ya hay barrera | Fuera | Trafficway = Divided, Barrier |
| Caso tipo | Derecha → sobrecorrige → cruza mediana → choque de frente | Dentro | Head On, Location = Roadway |

\* Supone que el Location está codificado como Roadside; vale la pena confirmarlo en ese reporte.

Limitaciones que hay que decir:
- El ancho de mediana (≤ 30 ft en la RDG) no está en los datos de choques; hay que cruzarlo con el inventario.
- Los choques de frente de alguien en sentido contrario (wrong-way) siguen entrando; no hay un campo de choque para sacarlos.

---

## 4. Lo más fuerte para la reunión: CMF vs. criteria

AASHTOWare aplica el CMF **solo** a los choques que pasan la criteria de la countermeasure. Si el CMF se midió en otro grupo, el beneficio sale mal. Es el problema de "51 % vs 13 %" de la reunión. Revisé los 133 treatments (Treatments, columnas AH-AI):

| Resultado | Cuántos | Qué significa |
|---|---|---|
| OK | 39 | El CMF mide los mismos choques |
| Understates | 57 | CMF para todos los tipos de choque aplicado a un grupo más chico: beneficio bajo (conservador) |
| **Overstates** | **25** | CMF medido en un grupo más chico (solo noche, solo giro derecho, solo cross-median…): **beneficio inflado** |
| Check | 7 | Otro tipo de choque o de vía; hay que decidir |
| Not used | 5 | Excluidos por el equipo |

Ejemplo que se entiende rápido: el selector, con "Lane Departure", recomienda en **#1 Median Barrier (97 %)**, y en #2 y #4 dos combinaciones de chevrons (79 % y 76.9 %). Las tres están infladas: el 97 % es solo para choques que cruzan la mediana, y las otras dos son solo de noche. Ahora el selector lo avisa en la columna "Read this before you use it".

Otros casos claros:
- **Lighting – Install Lighting (7784)**: el CMF es solo para alcances (rear-end), pero la criteria excluye rear-end. Se cancelan entre sí.
- **Systemic stop-controlled (8970)**: el CMF viene de intersecciones con semáforo.
- **Enhanced Delineation at Curves**: 5 de 9 CMFs son solo de noche.

## 5. Severidades (45 treatments)

El CMF estaba copiado en las cinco columnas K-A-B-C-O aunque el estudio solo midiera algunas. Ejemplo: 7718 es para KABC y también estaba reduciendo choques PDO; 2923 y 11524 son solo PDO y estaban reduciendo fatales.

Ahora la columna P guarda el CMF del estudio y K-O son fórmulas: si el estudio no cubre esa severidad, ponen 1.00 (sin efecto). Esto también resuelve lo que se habló en la reunión ("habría que crear otra countermeasure igual pero con criteria de lesionados"). No hace falta: con CMF = 1.00 en O el tratamiento solo actúa sobre lesionados.

---

## 6. Otros cambios por countermeasure (detalle en la hoja *Changes*)

- **PHB y RRFB** tenían criteria idéntica. Se separaron por velocidad y carriles según la guía STEP de FHWA (PHB: 35+ mph o 4+ carriles; RRFB: hasta 40 mph).
- **LPI y Walkways**: se quitaron filtros (giro y "caminando por la vía") porque sus CMFs son para todos los choques con peatón.
- **Enhanced Delineation at Curves**: propuse cambiar Roadway Departure por Lane Departure para que entren los choques de frente en la curva. **Es decisión del equipo.**
- **Road Diets**: AADT ≤ 20,000 (guía de Road Diet de FHWA). Se quitó la exclusión de freeways porque "Two-Way, Not Divided" ya las saca.
- **Pavement Friction**: solo Wet; ninguno de los 8 CMFs midió hielo. Además había un paréntesis que nunca cerraba.
- **Yellow Change Intervals**: en SC no hay código "Ran Red Light"; se usa Disregarded Sign/Signal.
- **Shoulder Rumble Strips, SafetyEdge y Wider Edge Lines** quedan con el mismo grupo de choques. Está bien así: son alternativas para los mismos choques y AASHTOWare las ordena por B/C.
- **Treatment Selector**: 133 fórmulas rotas (#REF!) en la columna de advertencias, porque se había borrado una columna en Treatments. Arregladas.

---

## 7. Revisar en el Condition Builder antes de presentar (unos 20 minutos)

Las etiquetas salen del diccionario de SC; estas no las vi en tu pantalla:

- [ ] **Traffic Control**: cómo dice exactamente "Traffic Signal" y "Stop Sign"
- [ ] **Road Character**: Curve-Level / Curve-On Grade / Curve-Hillcrest
- [ ] **Light Condition**: las 4 opciones de Dark. Antes se dijo que el SMS solo tenía Day/Night; el diccionario de SC tiene 7 valores. Conviene verlo en el dropdown.
- [ ] **Road Surface Condition = Wet**
- [ ] **Speed Limit** y **Area Type** bajo Roadway (AADT y carriles ya están confirmados)
- [ ] **Vehicle Maneuver / Turning Left**: nombre del campo de maniobra
- [ ] **Angle** en Manner of Collision: si sale tres veces (41, 42, 43), marcar las tres
- [ ] Probar Median Barriers en el builder con los paréntesis como grupo y comparar el conteo con tu query original

## 8. Preguntas abiertas para el equipo / Numetric

1. ¿"Speeding Related" incluye Too Fast for Conditions? Si no lo incluye, se puede usar el derivado.
2. ¿Lane Departure en vez de Roadway Departure para curvas?
3. Los 25 treatments con "Overstates": ¿se quitan, se separan en otra countermeasure (por ejemplo, curvas de noche) o se aceptan con nota?
4. Intersection Related está construido sobre Junction Type. Hoy funciona porque producción tiene el formato viejo, pero hay que rehacerlo cuando entren los reportes nuevos.

## 9. Lo que dice el MMUCC 6ª edición (hoja *New TR-310 (MMUCC 6)*)

Revisé el manual completo (DOT HS 813 525, revisión de febrero 2025). Confirma lo que ya está en las criteria del SMS y muestra lo que va a cambiar cuando los reportes nuevos lleguen a producción. La hoja nueva tiene las 30 criteria reescritas con campos MMUCC 6.

**Lo que confirma:**
- *Ran off road*, *Cross Median* y *Cross Centerline* **no son harmful events**. Solo existen en Sequence of Events (V37). Tu query original buscaba `Crash Harmful Event = Ran off Road Left` y `First Harmful Event = Cross Median/Center`: con datos MMUCC eso va a dar cero. La v8 ya usa Sequence of Events.
- Location of First Harmful Event (C8) sigue teniendo *On Median*, *On Roadside* y *On Shoulder*. El enfoque de median barriers por ubicación funciona igual en el formato nuevo.
- Speeding-Related (D5) separa *Racing*, *Exceeded Speed Limit* y *Too Fast for Conditions*. La decisión del equipo de enero 2025 se traduce uno a uno.

**Lo que cambia y hay que tener en cuenta:**
1. **Non-Junction ya no cubre las autopistas dentro de un intercambio.** En MMUCC 6, Relation to Junction (C12) usa *Through Roadway* para la vía principal dentro de un intercambio, y *Other Location Within an Interchange Area* para la mediana, el hombro y el borde. Si median barriers solo pide Non-Junction, se pierden todos esos choques. En la hoja MMUCC lo agrupé como "Segment". **También hay que revisar si hoy el Junction Type del SMS tiene valores de intercambio o rampa** (los códigos 06, 10 y 11 no salieron en el diccionario). Lo agregué como pendiente en Median Barriers.
2. **Peatón y ciclista ya no se separan en First Harmful Event.** Hay un solo valor, *Non-Motorist*; la diferencia está en Person Type (P5). Lo mismo con animales: *Live Animal*, sin separar venados.
3. **La mediana con barrera tiene su propio campo:** Median Barrier Presence (V26) reemplaza Trafficway 2 y 3. Trafficway Flow (V25) distingue *Two-Way With a Continuous Left-Turn Lane*, lo que sirve en Road Diets para no recomendar donde ya hay tres carriles.
4. **Las condiciones de la vía pasan a ser por vehículo:** superficie, alineamiento (vuelve *Curve Left / Curve Right*), control de tráfico, límite de velocidad, carriles, flujo y barrera. Con `=` funciona igual; con `≠` aplica la trampa del punto 2.3.
5. **No existe "Debris".** *Obstruction in Roadway* está en Related Factors – Crash Level (C17); los escombros salen como First Harmful Event = *Other Object (not fixed)*.
6. **Campos nuevos que resuelven pendientes de hoy:**
   - Walkways: Non-Motorist Status (NM2) = *Movement With / Against Traffic*. Es el filtro de "caminando por la vía" que hoy no se puede hacer.
   - LPI: Non-Motorist Traffic Control Device (NM10) = *Non-Motorist Crossing Signal*, porque el LPI necesita semáforo peatonal.
   - Crosswalks: Non-Motorist in Crosswalk (NM6) = *Yes, Marked / Unmarked*.
   - Yellow Change: Related Factors – Driver Level (D10) = *Failure to Obey Traffic Control Devices*.
   - SafetyEdge: D10 = *Overcorrecting*.
   - RCUT existentes: Type of Intersection = *Other Intersection Type*.
7. **Numetric tiene que rehacer los campos derivados** (Roadway Departure, Lane Departure, Intersection Related, Pedestrian) sobre estos campos. La definición propuesta está arriba en la hoja MMUCC.

Aviso: los nombres son los del MMUCC. El TR-310 nuevo de SC puede usar etiquetas un poco distintas.

---

### Lo que no pude hacer

- **Manual MMUCC:** ya revisado (6ª edición completa); ver sección 9.
- **Sin acceso a la red** del CMF Clearinghouse, Numetric ni NHTSA desde este entorno (el proxy los bloquea). Los códigos de SC salen de búsquedas sobre el diccionario de SCDPS 6/2010, y la revisión de CMFs se hizo con los datos que ya estaban en la hoja Treatments.
- **Sin datos de choques**, así que no corrí conteos. Las pruebas de la sección 3 son con los cuatro choques que ya habías revisado.
