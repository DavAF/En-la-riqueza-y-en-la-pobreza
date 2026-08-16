"""
==============================================================================
 EVALUADOR ECONÓMICO DE PAREJA — Marco de Gary Becker (Nobel Economía 1992)
==============================================================================
Basado en:
 - Gary S. Becker, "A Treatise on the Family" (1981) — ventaja comparativa
   doméstica, capital humano, mercado matrimonial, especialización conyugal.
 - Legislación civil española: Código Civil (arts. 97, 1315-1444) y derechos
   forales/autonómicos sobre régimen económico matrimonial supletorio.

AVISO IMPORTANTE
-----------------------------------------------------------------------------
Esta herramienta es un simulador ORIENTATIVO con fines educativos y de
planificación personal. NO constituye asesoramiento legal, fiscal ni
financiero profesional. La legislación cambia y varía según el caso
concreto (fecha de matrimonio, capitulaciones, vecindad civil, etc.).
Consulta siempre a un abogado de familia y/o asesor financiero colegiado.
==============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="Evaluador Económico de Pareja — Modelo Becker",
    page_icon="💍",
    layout="wide",
)

# =============================================================================
# DATOS DE REFERENCIA: RÉGIMEN ECONÓMICO MATRIMONIAL SUPLETORIO POR CCAA
# =============================================================================
# Simplificado. El régimen "supletorio" es el que se aplica si la pareja NO
# firma capitulaciones matrimoniales eligiendo otro. Fuente: Código Civil
# arts. 1316 y ss., y compilaciones forales (Cataluña, Aragón, Baleares,
# Navarra, País Vasco, Galicia).

REGIMEN_CCAA = {
    "Andalucía": {"regimen": "Sociedad de gananciales", "norma": "Código Civil (art. 1316 CC)"},
    "Aragón": {"regimen": "Consorcio conyugal (similar a gananciales)", "norma": "Código de Derecho Foral de Aragón"},
    "Asturias": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Baleares (Mallorca y Menorca)": {"regimen": "Separación de bienes", "norma": "Compilación de Derecho Civil de Baleares"},
    "Baleares (Ibiza y Formentera)": {"regimen": "Separación de bienes (con posible espolits)", "norma": "Compilación Balear"},
    "Canarias": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Cantabria": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Castilla-La Mancha": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Castilla y León": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Cataluña": {"regimen": "Separación de bienes", "norma": "Codi Civil de Catalunya, Llibre II"},
    "Comunidad Valenciana": {"regimen": "Sociedad de gananciales*", "norma": "Código Civil (tras STC 82/2016 que anuló la Ley 10/2007 valenciana)"},
    "Extremadura": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Galicia": {"regimen": "Sociedad de gananciales", "norma": "Ley 2/2006 de Derecho Civil de Galicia"},
    "La Rioja": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Madrid": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Murcia": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
    "Navarra": {"regimen": "Sociedad de conquistas", "norma": "Fuero Nuevo / Compilación de Navarra"},
    "País Vasco (Bizkaia - aforado)": {"regimen": "Comunicación foral de bienes", "norma": "Ley 5/2015 Derecho Civil Vasco"},
    "País Vasco (resto)": {"regimen": "Sociedad de gananciales", "norma": "Código Civil"},
}

def color_score(v):
    if v >= 70:
        return "🟢"
    elif v >= 45:
        return "🟡"
    else:
        return "🔴"

# =============================================================================
# SIDEBAR — Identificación de fase
# =============================================================================
st.sidebar.title("💍 Evaluador Económico de Pareja")
st.sidebar.caption("Marco teórico: **Gary S. Becker** — *A Treatise on the Family* (1981)")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "Selecciona la **pestaña** correspondiente a tu situación actual. "
    "Cada fase usa parámetros y fórmulas distintas."
)
ccaa = st.sidebar.selectbox("Comunidad Autónoma / territorio foral (para régimen económico)", list(REGIMEN_CCAA.keys()))
info = REGIMEN_CCAA[ccaa]
st.sidebar.info(f"**Régimen supletorio:** {info['regimen']}\n\n*Norma:* {info['norma']}")
st.sidebar.markdown("---")
st.sidebar.caption("⚠️ Herramienta orientativa. No sustituye asesoría legal/financiera profesional.")

st.title("Evaluador Económico de Pareja")
st.caption("Cuantificación basada en el modelo de capital humano, especialización y ventaja comparativa doméstica de Gary Becker.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ Candidata/o a pareja",
    "2️⃣ Noviazgo (metas comunes)",
    "3️⃣ Casados (vida conyugal)",
    "4️⃣ Jubilación",
    "5️⃣ Separación / Divorcio",
])

# =============================================================================
# TAB 1 — EVALUACIÓN DE CANDIDATA/O
# =============================================================================
with tab1:
    st.header("Fase 1 · Evaluación pre-relación (mercado matrimonial de Becker)")
    st.markdown(
        "Becker modela la elección de pareja como una decisión de **inversión en capital humano compartido**: "
        "se valora el *stock* actual de capital (activos, formación, salud) y su **potencial de crecimiento futuro**, "
        "no solo la renta presente."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Perfil personal")
        edad = st.number_input("Edad", 18, 80, 32, key="c_edad")
        formacion = st.selectbox("Nivel de formación", [
            "Sin estudios / ESO", "Bachillerato/FP medio", "FP superior",
            "Grado universitario", "Máster", "Doctorado"], index=3, key="c_form")
        profesion = st.text_input("Profesión", "Ingeniera/o", key="c_prof")
        sector = st.selectbox("Sector", [
            "Público (funcionariado)", "Tecnología", "Sanidad", "Educación",
            "Industria/Construcción", "Servicios/Comercio", "Finanzas/Legal",
            "Autónomo/Emprendimiento", "Otro"], key="c_sector")
        estabilidad_sector = st.slider("Estabilidad percibida del sector (1-10)", 1, 10, 6, key="c_estab")
    with c2:
        st.subheader("Capital económico y contingencias")
        activos = st.number_input("Activos netos actuales (€)", 0, 5_000_000, 20_000, step=1000, key="c_activos")
        ingresos = st.number_input("Ingresos netos anuales (€)", 0, 1_000_000, 24_000, step=500, key="c_ing")
        deudas = st.number_input("Deudas pendientes (€)", 0, 2_000_000, 0, step=500, key="c_deudas")
        herencia_prob = st.slider("Probabilidad de herencia futura relevante (%)", 0, 100, 20, key="c_herprob")
        herencia_valor = st.number_input("Valor estimado de esa herencia (€)", 0, 5_000_000, 0, step=5000, key="c_herval")
        relaciones_previas = st.number_input("Nº de relaciones largas previas (>2 años)", 0, 15, 1, key="c_rel")
        hijos_previos = st.number_input("Nº de hijos de relaciones anteriores", 0, 10, 0, key="c_hijosprev")
        salud = st.select_slider("Estado de salud general", 
            options=["Grave/crónico limitante", "Problema moderado", "Bueno", "Muy bueno", "Excelente"], value="Bueno", key="c_salud")

    # --- Cálculo del "Índice de Capital Conyugal Potencial" (ICCP) ---
    map_formacion = {"Sin estudios / ESO": 10, "Bachillerato/FP medio": 30, "FP superior": 50,
                      "Grado universitario": 70, "Máster": 85, "Doctorado": 95}
    map_salud = {"Grave/crónico limitante": 20, "Problema moderado": 55, "Bueno": 75, "Muy bueno": 90, "Excelente": 100}

    score_formacion = map_formacion[formacion]
    score_salud = map_salud[salud]
    score_economico = min(100, (activos - deudas) / 2000 + ingresos / 500)
    score_economico = max(0, score_economico)
    valor_esperado_herencia = herencia_valor * (herencia_prob / 100)
    score_herencia = min(100, valor_esperado_herencia / 3000)
    score_estabilidad = estabilidad_sector * 10
    penal_relaciones = min(20, relaciones_previas * 2 + hijos_previos * 3)

    ICCP = (
        score_formacion * 0.20 +
        score_economico * 0.25 +
        score_estabilidad * 0.15 +
        score_salud * 0.20 +
        score_herencia * 0.10 +
        (100 - penal_relaciones) * 0.10
    )
    ICCP = round(max(0, min(100, ICCP)), 1)

    st.markdown("---")
    r1, r2 = st.columns([1, 2])
    with r1:
        st.metric("Índice de Capital Conyugal Potencial (ICCP)", f"{ICCP}/100", delta=color_score(ICCP))
        st.caption("Combina capital humano (formación, salud), capital financiero y estabilidad esperada, "
                   "penalizando cargas de relaciones previas (enfoque Becker de coste de oportunidad).")
    with r2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ICCP,
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "darkblue"},
                   'steps': [{'range': [0, 45], 'color': "#f8d7da"},
                             {'range': [45, 70], 'color': "#fff3cd"},
                             {'range': [70, 100], 'color': "#d4edda"}]}))
        fig.update_layout(height=250, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    df_desglose = pd.DataFrame({
        "Componente": ["Formación", "Económico", "Estabilidad sector", "Salud", "Herencia esperada", "Historial relacional"],
        "Puntuación": [score_formacion, round(score_economico,1), score_estabilidad, score_salud, round(score_herencia,1), round(100-penal_relaciones,1)]
    })
    st.bar_chart(df_desglose.set_index("Componente"))

# =============================================================================
# TAB 2 — NOVIAZGO: METAS COMUNES
# =============================================================================
with tab2:
    st.header("Fase 2 · Noviazgo — Negociación de metas comunes")
    st.markdown(
        "Becker plantea el matrimonio como una **empresa conjunta con ganancias de la especialización**: "
        "cada miembro se especializa donde tiene ventaja comparativa (mercado laboral vs. producción doméstica). "
        "Aquí se modela la viabilidad económica de las metas comunes típicas del noviazgo."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Ingresos y ahorro combinados")
        ing_a = st.number_input("Ingresos netos anuales — persona A (€)", 0, 1_000_000, 28_000, step=500, key="n_ingA")
        ing_b = st.number_input("Ingresos netos anuales — persona B (€)", 0, 1_000_000, 24_000, step=500, key="n_ingB")
        ahorro_a = st.number_input("Ahorro actual — persona A (€)", 0, 2_000_000, 15_000, step=500, key="n_ahA")
        ahorro_b = st.number_input("Ahorro actual — persona B (€)", 0, 2_000_000, 10_000, step=500, key="n_ahB")
        tasa_ahorro_mensual = st.slider("% de ingresos conjuntos destinado a ahorro mensual", 0, 60, 15, key="n_tasa")
    with c2:
        st.subheader("Metas comunes")
        precio_piso = st.number_input("Precio objetivo de vivienda (€)", 0, 3_000_000, 220_000, step=5000, key="n_piso")
        entrada_pct = st.slider("% de entrada exigido (habitual 20%)", 5, 40, 20, key="n_entrada")
        num_hijos = st.number_input("Número de hijos deseados", 0, 6, 2, key="n_hijos")
        coste_hijo_anual = st.number_input("Coste medio anual estimado por hijo (€)", 0, 50_000, 6_000, step=500, key="n_costehijo")
        horizonte_boda = st.slider("Años hasta la boda deseada", 0, 10, 2, key="n_horizonte")
        presupuesto_boda = st.number_input("Presupuesto boda (€)", 0, 200_000, 15_000, step=500, key="n_boda")

    st.subheader("Evolución profesional prevista durante el noviazgo")
    c3, c4 = st.columns(2)
    with c3:
        evolucion_a = st.selectbox("Trayectoria esperada — persona A", ["Fuerte crecimiento", "Crecimiento moderado", "Estable", "Riesgo de involución"], key="n_evolA")
    with c4:
        evolucion_b = st.selectbox("Trayectoria esperada — persona B", ["Fuerte crecimiento", "Crecimiento moderado", "Estable", "Riesgo de involución"], key="n_evolB")

    # --- Cálculos ---
    ingresos_totales = ing_a + ing_b
    ahorro_mensual = ingresos_totales * (tasa_ahorro_mensual / 100) / 12
    ahorro_actual_total = ahorro_a + ahorro_b
    entrada_necesaria = precio_piso * (entrada_pct / 100) + precio_piso * 0.10  # +10% gastos/impuestos aprox.
    falta_para_entrada = max(0, entrada_necesaria - ahorro_actual_total)
    meses_para_piso = falta_para_entrada / ahorro_mensual if ahorro_mensual > 0 else float("inf")

    coste_hijos_total_10y = num_hijos * coste_hijo_anual * 10
    coste_boda_mensual_necesario = presupuesto_boda / max(1, horizonte_boda * 12)

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Ahorro mensual conjunto", f"{ahorro_mensual:,.0f} €")
    m2.metric("Entrada + gastos vivienda necesarios", f"{entrada_necesaria:,.0f} €")
    m3.metric("Tiempo estimado hasta entrada", f"{meses_para_piso:.0f} meses" if meses_para_piso != float("inf") else "No viable con ahorro actual")
    m4.metric("Coste estimado hijos (10 años)", f"{coste_hijos_total_10y:,.0f} €")

    if meses_para_piso <= horizonte_boda * 12 or meses_para_piso == 0:
        st.success("✅ La meta de vivienda es alcanzable dentro del horizonte de boda planteado.")
    elif meses_para_piso < float("inf"):
        st.warning(f"⚠️ Al ritmo actual de ahorro, la vivienda se alcanza en {meses_para_piso/12:.1f} años, "
                    f"más tarde que el horizonte de boda ({horizonte_boda} años). Considerad ajustar tasa de ahorro o presupuesto.")
    else:
        st.error("🔴 Con la tasa de ahorro actual (0%) la meta de vivienda no es alcanzable. Definid un % de ahorro.")

    riesgo_map = {"Fuerte crecimiento": 1, "Crecimiento moderado": 0.5, "Estable": 0, "Riesgo de involución": -1}
    balance_evolucion = riesgo_map[evolucion_a] + riesgo_map[evolucion_b]
    if balance_evolucion >= 1:
        st.info("📈 Balance de trayectorias profesionales positivo: la pareja tiene margen para asumir hijos/vivienda con proyección de ingresos crecientes (lógica Becker de inversión en capital humano futuro).")
    elif balance_evolucion <= -1:
        st.warning("📉 Riesgo de involución profesional conjunta: conviene priorizar fondo de emergencia antes de comprometer metas de alto coste fijo (hijos, hipoteca).")

# =============================================================================
# TAB 3 — CASADOS: VIDA CONYUGAL
# =============================================================================
with tab3:
    st.header("Fase 3 · Matrimonio — Gestión económica conjunta")
    st.markdown(
        f"Régimen económico aplicable en **{ccaa}**: **{info['regimen']}** ({info['norma']}). "
        "Recuerda que mediante capitulaciones matrimoniales podéis pactar otro régimen distinto al supletorio."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Situación actual")
        ingresos_hogar = st.number_input("Ingresos netos anuales del hogar (€)", 0, 2_000_000, 60_000, step=1000, key="m_ing")
        patrimonio_neto = st.number_input("Patrimonio neto conjunto (€)", -500_000, 5_000_000, 80_000, step=1000, key="m_patr")
        gasto_colegio_actual = st.number_input("Gasto anual actual en educación de hijos (€)", 0, 100_000, 0, step=500, key="m_colegio")
        gasto_colegio_deseado = st.number_input("Gasto anual deseado (mejora de colegio) (€)", 0, 100_000, 6_000, step=500, key="m_colegiodes")
    with c2:
        st.subheader("Cambios deseados")
        cambio_barrio = st.selectbox("¿Cambio de barrio/vivienda?", ["No", "Sí, a zona similar", "Sí, a zona más cara", "Sí, a zona más económica"], key="m_barrio")
        coste_cambio_barrio = st.number_input("Coste extra estimado del cambio (mudanza, hipoteca, etc.) (€)", 0, 1_000_000, 0, step=1000, key="m_costebarrio")
        presupuesto_vacaciones = st.number_input("Presupuesto vacaciones deseado anual (€)", 0, 100_000, 3000, step=200, key="m_vac")
        cambio_sector = st.checkbox("¿Alguien planea cambio de sector profesional?", key="m_cambiosector")
        anio_sabatico = st.checkbox("¿Se plantea año sabático?", key="m_sabatico")
        meses_sabatico = st.slider("Meses de año sabático", 0, 24, 6, key="m_mesessab") if anio_sabatico else 0
        perdida_ingresos_sabatico_pct = st.slider("% de ingresos que se perderían durante el sabático", 0, 100, 80, key="m_pctsab") if anio_sabatico else 0

    gasto_extra_colegio = gasto_colegio_deseado - gasto_colegio_actual
    coste_sabatico = ingresos_hogar * (meses_sabatico/12) * (perdida_ingresos_sabatico_pct/100)
    gasto_anual_extra_total = max(0, gasto_extra_colegio) + coste_cambio_barrio/10 + presupuesto_vacaciones

    st.markdown("---")
    st.subheader("Impacto económico anual de los cambios propuestos")
    m1, m2, m3 = st.columns(3)
    m1.metric("Extra anual en educación", f"{max(0,gasto_extra_colegio):,.0f} €")
    m2.metric("Coste amortizado del cambio de barrio (10 años)", f"{coste_cambio_barrio/10:,.0f} €/año")
    m3.metric("Coste de oportunidad año sabático", f"{coste_sabatico:,.0f} €")

    capacidad_pct = (gasto_anual_extra_total / ingresos_hogar * 100) if ingresos_hogar > 0 else 0
    st.progress(min(1.0, capacidad_pct/100))
    if capacidad_pct < 15:
        st.success(f"🟢 Los cambios deseados suponen ~{capacidad_pct:.1f}% de los ingresos anuales: sostenibles.")
    elif capacidad_pct < 30:
        st.warning(f"🟡 Los cambios suponen ~{capacidad_pct:.1f}% de los ingresos anuales: viable con ajustes.")
    else:
        st.error(f"🔴 Los cambios suponen ~{capacidad_pct:.1f}% de los ingresos anuales: revisar prioridades o escalonar en el tiempo.")

    if cambio_sector:
        st.info("💼 Un cambio de sector implica pérdida temporal de ingresos y capital humano específico (Becker): "
                "valorad el ROI esperado (nuevo salario × probabilidad de éxito) frente al coste de reentrenamiento.")

# =============================================================================
# TAB 4 — JUBILACIÓN
# =============================================================================
with tab4:
    st.header("Fase 4 · Planificación de la jubilación")
    st.markdown(
        "Becker enfatiza la acumulación de capital (humano y financiero) a lo largo del ciclo vital de la familia. "
        "Esta pestaña proyecta el ahorro conjunto hasta la jubilación, combinando aportaciones y régimen público."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Persona A")
        edad_a = st.number_input("Edad actual A", 18, 70, 35, key="j_edadA")
        jub_a = st.number_input("Edad de jubilación deseada A", 55, 75, 67, key="j_jubA")
        salario_a = st.number_input("Salario bruto anual A (€)", 0, 1_000_000, 30_000, step=500, key="j_salA")
        ahorro_actual_a = st.number_input("Ahorro/planes de pensiones actuales A (€)", 0, 3_000_000, 10_000, step=500, key="j_ahA")
        aportacion_a = st.number_input("Aportación mensual a jubilación A (€)", 0, 20_000, 150, step=10, key="j_apA")
        anios_cotizados_a = st.number_input("Años ya cotizados a la Seguridad Social A", 0, 50, 10, key="j_cotA")
    with c2:
        st.subheader("Persona B")
        edad_b = st.number_input("Edad actual B", 18, 70, 33, key="j_edadB")
        jub_b = st.number_input("Edad de jubilación deseada B", 55, 75, 67, key="j_jubB")
        salario_b = st.number_input("Salario bruto anual B (€)", 0, 1_000_000, 26_000, step=500, key="j_salB")
        ahorro_actual_b = st.number_input("Ahorro/planes de pensiones actuales B (€)", 0, 3_000_000, 8_000, step=500, key="j_ahB")
        aportacion_b = st.number_input("Aportación mensual a jubilación B (€)", 0, 20_000, 150, step=10, key="j_apB")
        anios_cotizados_b = st.number_input("Años ya cotizados a la Seguridad Social B", 0, 50, 8, key="j_cotB")

    rentabilidad_anual = st.slider("Rentabilidad media anual esperada de las inversiones (%)", 0.0, 10.0, 4.0, step=0.5, key="j_rent") / 100
    inflacion = st.slider("Inflación media estimada (%)", 0.0, 8.0, 2.5, step=0.5, key="j_infl") / 100

    def proyeccion_jubilacion(edad, edad_jub, ahorro_ini, aportacion_mensual, rent):
        anios = max(0, edad_jub - edad)
        capital = ahorro_ini
        historial = [capital]
        for _ in range(anios):
            capital = capital * (1 + rent) + aportacion_mensual * 12
            historial.append(capital)
        return capital, historial, anios

    capital_final_a, hist_a, anios_a = proyeccion_jubilacion(edad_a, jub_a, ahorro_actual_a, aportacion_a, rentabilidad_anual)
    capital_final_b, hist_b, anios_b = proyeccion_jubilacion(edad_b, jub_b, ahorro_actual_b, aportacion_b, rentabilidad_anual)

    # Estimación MUY simplificada de pensión pública (base reguladora orientativa: 2% por año cotizado, tope 100% con 37 años)
    def pension_publica_estimada(salario, anios_cotizados_total):
        base_reguladora_mensual = salario / 14  # aprox. pagas
        pct = min(100, anios_cotizados_total * 2.7)  # aproximación normativa post-reforma, orientativa
        return base_reguladora_mensual * (pct / 100)

    pension_a = pension_publica_estimada(salario_a, anios_cotizados_a + anios_a)
    pension_b = pension_publica_estimada(salario_b, anios_cotizados_b + anios_b)

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Capital privado proyectado A", f"{capital_final_a:,.0f} €")
    m2.metric("Capital privado proyectado B", f"{capital_final_b:,.0f} €")
    m3.metric("Pensión pública mensual estimada A", f"{pension_a:,.0f} €/mes")
    m4.metric("Pensión pública mensual estimada B", f"{pension_b:,.0f} €/mes")

    st.caption("⚠️ La fórmula de pensión pública es una aproximación simplificada del sistema contributivo español "
               "(bases reguladoras y porcentajes reales dependen de la Ley General de la Seguridad Social, "
               "años exactos cotizados y bases de cotización). Consulta tu 'vida laboral' y simulador oficial de la Seguridad Social.")

    df_proy = pd.DataFrame({
        "Año": list(range(len(hist_a))),
        "Persona A": hist_a,
    })
    df_proy_b = pd.DataFrame({"Año": list(range(len(hist_b))), "Persona B": hist_b})
    fig = px.line(title="Proyección de capital acumulado hasta jubilación")
    fig.add_scatter(x=df_proy["Año"], y=df_proy["Persona A"], name="Persona A", mode="lines")
    fig.add_scatter(x=df_proy_b["Año"], y=df_proy_b["Persona B"], name="Persona B", mode="lines")
    fig.update_layout(xaxis_title="Años desde hoy", yaxis_title="Capital acumulado (€)")
    st.plotly_chart(fig, use_container_width=True)

    capital_conjunto = capital_final_a + capital_final_b
    ingreso_mensual_conjunto = pension_a + pension_b + (capital_conjunto * 0.04 / 12)  # regla del 4%
    st.metric("Ingreso mensual conjunto estimado en jubilación (pensión + retiro 4% capital privado)", f"{ingreso_mensual_conjunto:,.0f} €/mes")

# =============================================================================
# TAB 5 — SEPARACIÓN / DIVORCIO
# =============================================================================
with tab5:
    st.header("Fase 5 · Separación / Divorcio — Liquidación económica")
    st.markdown(
        f"Cálculo orientativo según régimen **{info['regimen']}** ({ccaa}) y arts. 90-101 del Código Civil "
        "(pensión compensatoria, pensión de alimentos, atribución de vivienda)."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Datos económicos")
        patrimonio_comun = st.number_input("Patrimonio común a liquidar (€)", 0, 10_000_000, 150_000, step=1000, key="d_patrimonio")
        ingresos_a_d = st.number_input("Ingresos netos anuales — parte A (€)", 0, 1_000_000, 35_000, step=500, key="d_ingA")
        ingresos_b_d = st.number_input("Ingresos netos anuales — parte B (€)", 0, 1_000_000, 20_000, step=500, key="d_ingB")
        anios_matrimonio = st.number_input("Años de matrimonio", 0, 60, 8, key="d_anios")
        desequilibrio_generado = st.checkbox("¿Hubo renuncia/reducción de carrera profesional de una parte por el hogar/hijos?", key="d_desequilibrio")
    with c2:
        st.subheader("Hijos y vivienda")
        hijos_comunes = st.number_input("Nº de hijos comunes menores/dependientes", 0, 10, 1, key="d_hijos")
        custodia = st.selectbox("Tipo de custodia previsto", ["Compartida", "Monoparental — parte A", "Monoparental — parte B"], key="d_custodia")
        valor_vivienda = st.number_input("Valor de la vivienda habitual (€)", 0, 5_000_000, 200_000, step=5000, key="d_vivienda")
        hipoteca_pendiente = st.number_input("Hipoteca pendiente (€)", 0, 5_000_000, 90_000, step=1000, key="d_hipoteca")

    # --- Reparto según régimen ---
    if "gananciales" in info["regimen"].lower() or "conquistas" in info["regimen"].lower() or "consorcio" in info["regimen"].lower() or "comunicación" in info["regimen"].lower():
        reparto_a = patrimonio_comun / 2
        reparto_b = patrimonio_comun / 2
        nota_regimen = "Reparto al 50% del patrimonio ganancial (bienes adquiridos durante el matrimonio), salvo bienes privativos acreditados."
    else:
        reparto_a = patrimonio_comun * (ingresos_a_d / max(1, (ingresos_a_d + ingresos_b_d)))
        reparto_b = patrimonio_comun * (ingresos_b_d / max(1, (ingresos_a_d + ingresos_b_d)))
        nota_regimen = "En separación de bienes cada parte conserva lo suyo; el reparto mostrado es solo una aproximación para bienes en proindiviso, proporcional a la aportación."

    equidad_vivienda = valor_vivienda - hipoteca_pendiente

    # --- Pensión de alimentos (muy orientativa: % ingresos del no custodio según nº hijos) ---
    pct_alimentos_map = {1: 0.20, 2: 0.30, 3: 0.35}
    pct_alimentos = pct_alimentos_map.get(min(hijos_comunes, 3), 0.35 + 0.03*(hijos_comunes-3)) if hijos_comunes > 0 else 0
    if custodia == "Monoparental — parte A":
        pagador, pagador_ingresos = "B", ingresos_b_d
    elif custodia == "Monoparental — parte B":
        pagador, pagador_ingresos = "A", ingresos_a_d
    else:
        pagador, pagador_ingresos = None, None

    pension_alimentos_anual = pagador_ingresos * pct_alimentos if pagador_ingresos else 0

    # --- Pensión compensatoria (art. 97 CC): orientativa, función de desequilibrio y años de matrimonio ---
    diferencia_ingresos = abs(ingresos_a_d - ingresos_b_d)
    pension_compensatoria_anual = 0
    duracion_orientativa = 0
    if desequilibrio_generado and diferencia_ingresos > 0:
        pension_compensatoria_anual = diferencia_ingresos * 0.25
        duracion_orientativa = round(anios_matrimonio / 2)

    st.markdown("---")
    st.subheader("Resultado de la liquidación económica")
    m1, m2, m3 = st.columns(3)
    m1.metric("Reparto patrimonio — parte A", f"{reparto_a:,.0f} €")
    m2.metric("Reparto patrimonio — parte B", f"{reparto_b:,.0f} €")
    m3.metric("Equidad neta vivienda (valor - hipoteca)", f"{equidad_vivienda:,.0f} €")
    st.caption(nota_regimen)

    if hijos_comunes > 0 and pagador:
        st.warning(f"👨‍👩‍👧 Pensión de alimentos orientativa a cargo de la parte {pagador} ({pct_alimentos*100:.0f}% de sus ingresos netos, según nº de hijos)")
        st.metric(f"Pensión de alimentos estimada (parte {pagador} → hijos)", f"{pension_alimentos_anual/12:,.0f} €/mes")
    elif hijos_comunes > 0:
        st.info("Con custodia compartida, los gastos ordinarios suelen repartirse proporcionalmente a ingresos; "
                "no se calcula pensión de alimentos entre partes salvo desequilibrio de ingresos.")

    if pension_compensatoria_anual > 0:
        st.metric("Pensión compensatoria estimada (art. 97 CC)", f"{pension_compensatoria_anual/12:,.0f} €/mes durante ~{duracion_orientativa} años")
        st.caption("Estimación orientativa basada en diferencia de ingresos y desequilibrio derivado del reparto de roles durante el matrimonio "
                   "(coste de oportunidad de capital humano no invertido en el mercado laboral — enfoque Becker).")
    else:
        st.info("No se estima pensión compensatoria (no se ha marcado desequilibrio profesional generado durante el matrimonio, o ingresos similares).")

    st.markdown("---")
    df_reparto = pd.DataFrame({"Parte": ["A", "B"], "Patrimonio recibido (€)": [reparto_a, reparto_b]})
    fig2 = px.pie(df_reparto, names="Parte", values="Patrimonio recibido (€)", title="Reparto patrimonial estimado")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption(
    "📚 Marco teórico: Gary S. Becker, *A Treatise on the Family*, Harvard University Press, 1981 (Premio Nobel de "
    "Economía 1992). Legislación: Código Civil español y compilaciones forales de Aragón, Baleares, Cataluña, "
    "Galicia, Navarra y País Vasco. Cifras y porcentajes de esta app son **estimaciones orientativas** — no "
    "constituyen asesoramiento legal ni financiero."
)
