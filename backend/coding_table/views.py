# backend/coding_table/views.py
from django.http import JsonResponse
from .utils.csv_processing import process_csv, generate_coding_table

def process_and_generate_table(request):
    if request.method == 'POST':
        # Vérifier si un fichier a été envoyé avec la requête
        csv_file = request.FILES.get('csv_file')
        if csv_file:
            # Traiter le fichier CSV
            data = process_csv(csv_file)
            coding_table = generate_coding_table(data)
            
            # Envoyer la réponse JSON avec un message de succès
            return JsonResponse({'message': 'Tableau de codage généré avec succès.'})
        else:
            return JsonResponse({'error': 'Aucun fichier CSV envoyé.'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)
