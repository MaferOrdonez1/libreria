import clips

environment = clips.Environment()

class Regla:
    def __init__(self, condiciones, conclusion):
        self.condiciones = condiciones
        self.conclusion = conclusion

def definir_hechos_y_reglas(hechos, reglas):
    environment.clear()
    
    for hecho in hechos:
        environment.assert_string(f"(hecho {hecho})")

    for idx, regla in enumerate(reglas):
        condiciones = " ".join([f"(hecho {cond})" for cond in regla.condiciones])
        environment.build(f"""
        (defrule regla-{idx + 1}
            {condiciones}
            =>
            (assert (conclusion "{regla.conclusion}")))
        """)

def obtener_conclusiones():
    conclusiones = set()
    
    environment.run()
    
    for fact in environment.facts():
        fact_str = str(fact)
        if fact_str.startswith("(conclusion "):
            conclusion = fact_str.split('"')[1]
            conclusiones.add(conclusion)
    
    return conclusiones

def main():
    reglas = [
        Regla({"drama", "larga"}, "The Shawshank Redemption"),
        Regla({"drama", "corta"}, "Forrest Gump"),
        Regla({"comedia", "corta"}, "The Big Sick"),
        Regla({"comedia", "larga"}, "The Wolf of Wall Street"),
        Regla({"ciencia ficcion", "larga"}, "Inception"),
        Regla({"ciencia ficcion", "corta"}, "Edge of Tomorrow"),
    ]

    print("¡Bienvenido al Sistema Experto de Recomendación de Películas!\n")
    conclusiones_acumuladas = set()

    while True:
        print("Por favor, responde las siguientes preguntas sobre tus preferencias:")
        
        print("\nGéneros disponibles:")
        print("- Drama")
        print("- Comedia")
        print("- Ciencia Ficción")
        genero = input("¿Qué género prefieres? ").strip().lower()

        generos_disponibles = {"drama", "comedia", "ciencia ficcion"}
        if genero not in generos_disponibles:
            print("Género no reconocido. Por favor, elige uno de los géneros listados.")
            continue

        print("\nDuraciones disponibles:")
        print("- Corta (menos de 120 minutos)")
        print("- Larga (120 minutos o más)")
        duracion = input("¿Prefieres películas de duración corta o larga? ").strip().lower()

        duraciones_disponibles = {"corta", "larga"}
        if duracion not in duraciones_disponibles:
            print("Duración no reconocida. Por favor, elige 'corta' o 'larga'.")
            continue
        
        hechos = {genero, duracion}
        definir_hechos_y_reglas(hechos, reglas)

        recomendaciones = obtener_conclusiones()
        conclusiones_acumuladas.update(recomendaciones)

        if recomendaciones:
            print("\n¡Te recomendamos ver la siguiente película: ")
            for pelicula in recomendaciones:
                print(f"- {pelicula}")
        else:
            print("\nLo siento, no se encontró una recomendación basada en tus preferencias.")

        while True:
            respuesta = input("\n¿Deseas realizar otra recomendación? (s/n): ").strip().lower()
            if respuesta == "s":
                break
            elif respuesta == "n":
                print("\nGracias por usar el Sistema Experto de Recomendación de Películas.")
                if conclusiones_acumuladas:
                    print("\nConclusiones acumuladas durante la sesión:")
                    for pelicula in conclusiones_acumuladas:
                        print(f"- {pelicula}")
                else:
                    print("\nNo se derivaron recomendaciones durante la sesión.")
                return
            else:
                print("Respuesta no válida. Por favor, ingresa 's' para sí o 'n' para no.")

if __name__ == "__main__":
    main()
