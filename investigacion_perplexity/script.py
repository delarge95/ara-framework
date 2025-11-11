
import pandas as pd
import json

# Crear tabla comparativa maestra con datos de noviembre 2025
benchmarks_data = {
    'Modelo': [
        'GPT-5',
        'GPT-5-Codex',
        'GPT-5 mini',
        'Claude Sonnet 4.5',
        'Claude Haiku 4.5',
        'Gemini 2.5 Pro',
        'DeepSeek V3',
        'MiniMax-M2',
        'Qwen 2.5 Coder 32B',
        'o1/o3 (reasoning)',
        'GPT-4o',
        'GPT-4.1',
        'Grok Code Fast 1'
    ],
    'Proveedor': [
        'OpenAI', 'OpenAI', 'OpenAI', 'Anthropic', 'Anthropic',
        'Google', 'DeepSeek', 'MiniMax', 'Alibaba', 'OpenAI',
        'OpenAI', 'OpenAI', 'xAI'
    ],
    'Contexto': [
        '400K', '400K', '128K', '200K', '200K',
        '1M', '128K', '200K+', '128K', '128K',
        '128K', '128K', '128K'
    ],
    'Costo ($/1M tokens)': [
        '$1.25 / $10',
        '1 crédito',
        '0 / $1',
        '$3 / $15',
        '$1 / $5',
        '$1.25 / $5-10',
        'Gratis',
        'Gratis',
        'Gratis',
        '1-2 créditos',
        'Gratis',
        '0 / $1',
        '0.25 crédito'
    ],
    'HumanEval %': [
        '~92',
        '~94',
        '~85',
        '~85',
        '~80',
        '~90',
        '~92',
        '~83',
        '~87',
        '~95',
        '~88',
        '~87',
        '~82'
    ],
    'MMLU %': [
        '88.7',
        '~90',
        '~87',
        '~88',
        '~82',
        '86',
        '~88',
        '~95*',
        '~86',
        '~92',
        '~88.7',
        '~88',
        '~85'
    ],
    'SWE-Bench Verified %': [
        '72.8',
        '~75',
        '~70',
        '77.2',
        '73.3',
        '63.8',
        '67.8',
        '69.4',
        '~72',
        '74.9',
        '~68',
        '~68',
        '~65'
    ],
    'Terminal-Bench %': [
        '43.8',
        '~45',
        '~40',
        '50',
        '~42',
        '25.3',
        '37.7',
        '46.3',
        '~38',
        '~48',
        '~40',
        '~38',
        '~35'
    ],
    'Latencia (ms)': [
        '1500-2000',
        '1800-2200',
        '800-1200',
        '1200-1600',
        '600-1000',
        '2000-3000',
        '1000-1500',
        '800-1200',
        '1000-1500',
        '3000-5000',
        '1200-1600',
        '1200-1500',
        '400-800'
    ],
    'Disponibilidad': [
        'Copilot Pro+/Copilot Chat',
        'Copilot Pro+/VSCode',
        'Copilot Pro/Chat',
        'Copilot Pro+/API',
        'Copilot Pro/API',
        'Google AI Studio (gratis)',
        'OpenRouter (gratis)',
        'API gratis + Open-source',
        'API gratis',
        'Copilot Pro+',
        'Copilot Chat (gratis)',
        'Copilot Pro/Chat',
        'Copilot Pro'
    ]
}

df_benchmarks = pd.DataFrame(benchmarks_data)

# Tabla de pricing detallado
pricing_data = {
    'Modelo': [
        'GitHub Copilot Pro',
        'GitHub Copilot Pro+',
        'Claude Haiku 4.5 (API)',
        'Claude Sonnet 4.5 (API)',
        'GPT-5 (API)',
        'Gemini 2.5 Pro (gratis)',
        'DeepSeek V3 (gratis)',
        'MiniMax-M2 (gratis)',
        'Cursor Pro',
        'Continue.dev (gratis)',
        'Cody Sourcegraph (gratis)'
    ],
    'Costo Mensual': [
        '$10',
        '$39',
        'Pago por uso',
        'Pago por uso',
        'Pago por uso',
        'Gratis',
        'Gratis',
        'Gratis',
        '$20',
        'Gratis',
        'Gratis'
    ],
    'Créditos/Requests': [
        '300 premium/mes',
        '1,500 premium/mes',
        'Ilimitado',
        'Ilimitado',
        'Ilimitado',
        'Rate limits (RPM/TPM)',
        'Rate limits',
        'Ilimitado',
        '500 premium',
        'Ilimitado',
        'Ilimitado'
    ],
    'Costo Extra por Request': [
        '$0.04 c/u',
        '$0.04 c/u',
        'Incluido',
        'Incluido',
        'Incluido',
        'Incluido',
        'Incluido',
        'Incluido',
        '$0.10 c/u',
        'Incluido',
        'Incluido'
    ],
    'Modelos Disponibles': [
        'GPT-4o, Claude Haiku, Gemini',
        'Todo (incl. GPT-5, o3, Claude Opus)',
        'Haiku 4.5 solamente',
        'Sonnet 4.5 solamente',
        'GPT-5, GPT-5-Codex, minimax',
        'Gemini 2.5 Pro/Flash',
        'DeepSeek V3',
        'MiniMax-M2',
        'Claude Sonnet, GPT-4o',
        'Customizable (40+ providers)',
        'Claude 3.5, GPT-4o'
    ]
}

df_pricing = pd.DataFrame(pricing_data)

# Análisis de costos para 100 análisis/mes
cost_scenarios = {
    'Escenario': [
        'Conservador',
        'Balanceado',
        'Premium'
    ],
    'Descripción': [
        '80% gratis (Gemini/DeepSeek), 20% Haiku en Copilot',
        '40% gratis, 40% Haiku 4.5, 20% premium selectivo',
        'Mix óptimo: Sonnet para coding, GPT-5 para análisis, gratis para broker'
    ],
    'Stack de Modelos': [
        'Gemini 2.5 Pro + DeepSeek V3 + Haiku (300 créditos)',
        'Mismo + Copilot Pro ($10)',
        'Copilot Pro+ ($39) + Claude Sonnet API ($150-200)'
    ],
    'Costo Mensual': [
        '$0-5 (gratis + créditos sobrantes)',
        '$10-15',
        '$189-239'
    ],
    'Disponibilidad Modelos': [
        'Limitada (falta reasoning premium)',
        'Balanceada',
        'Máxima (acceso a todos los premium)'
    ],
    'Recomendación': [
        'Para MVP/inicial',
        'RECOMENDADO para ARA v1',
        'Para escala > 500 análisis/mes'
    ]
}

df_cost = pd.DataFrame(cost_scenarios)

print("=== TABLA COMPARATIVA MAESTRA ===")
print(df_benchmarks.to_string())
print("\n=== PRICING ===")
print(df_pricing.to_string())
print("\n=== ANÁLISIS DE COSTOS ===")
print(df_cost.to_string())

# Exportar a CSV
df_benchmarks.to_csv('benchmarks_modelos_nov2025.csv', index=False)
df_pricing.to_csv('pricing_comparativo_nov2025.csv', index=False)
df_cost.to_csv('escenarios_costos.csv', index=False)

print("\n✓ Archivos CSV generados")
