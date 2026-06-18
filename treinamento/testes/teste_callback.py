from callbacks import criar_callbacks

callbacks = criar_callbacks()

print()

for callback in callbacks:
    print(type(callback).__name__)

print("\nCallbacks carregados com sucesso!")