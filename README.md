# Demo DevSecOps — TPI ASI 2026 (UTN FRLP)

Aplicación web mínima (Flask + SQLite en memoria) con un pipeline de GitHub Actions
que ejecuta controles de seguridad automáticos y **bloquea la publicación** si encuentra
problemas de severidad alta o crítica.

> La versión de este repositorio tiene **vulnerabilidades intencionales**. Es a propósito:
> sirven para mostrar cómo el pipeline las detecta.

## Estructura

```
app/app.py                      Aplicación (4 rutas)
app/requirements.txt            Dependencias
Dockerfile                      Imagen de contenedor
.github/workflows/devsecops.yml Pipeline DevSecOps
```

## Vulnerabilidades intencionales y quién las detecta

| # | Vulnerabilidad | Dónde | Herramienta |
|---|---|---|---|
| 1 | Token de administrador escrito en el código | `app.py` | Gitleaks |
| 2 | Consulta SQL armada concatenando texto (inyección SQL) | `app.py` | Bandit (B608) |
| 3 | Flask en modo debug | `app.py` | Bandit (B201) |
| 4 | Flask y Werkzeug 2.2.2 con CVE de severidad alta | `requirements.txt` | Trivy (SCA) |
| 5 | Imagen base vieja y proceso corriendo como root | `Dockerfile` | Trivy (config e imagen) |

## Etapas del pipeline

1. **analisis-codigo**: Gitleaks (secretos), Bandit (SAST), Trivy fs (dependencias), Trivy config (Dockerfile).
2. **imagen** (en paralelo): construye la imagen, la escanea con Trivy y genera el SBOM (CycloneDX).
3. **dast**: solo si 1 y 2 pasaron. Levanta la app y la analiza con ZAP baseline.
4. **publicar**: solo si todo pasó (publicación simulada).

Los reportes (Bandit, SBOM, ZAP) quedan como *artifacts* en cada ejecución.

## Probar la app en tu compu (opcional)

```bash
cd app
pip install -r requirements.txt
python app.py
# abrir http://localhost:5000
```

Demostración de la inyección SQL (en la versión vulnerable devuelve **todos** los productos):

```
http://localhost:5000/productos?nombre=zzz' OR 1=1 --
http://localhost:5000/productos?nombre=zzz' UNION SELECT 1, sqlite_version(), 0 --
```

## Notas

- Las acciones de terceros están fijadas por hash de commit (SHA). Ver el caso de
  Trivy de marzo de 2026 en el trabajo escrito.
- En un proyecto real, un secreto que llegó a un commit **debe rotarse** aunque después
  se borre del código, porque queda en el historial de Git.
