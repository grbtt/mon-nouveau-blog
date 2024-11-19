from .models import Character,Equipement
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from django.contrib import messages 

def character_list(request):
        characters = Character.objects.all()
        equipements =Equipement.objects.all()
        return render(request, 'playground/character_list.html', {'characters': characters, 'equipements': equipements})

def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    return render(request, 'playground/equipement_detail.html', {'equipement': equipement})

def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = character.lieu  
    
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)  
        if form.is_valid():
            character = form.save(commit=False)
            if character.lieu.disponibilite == "libre":
                nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
                if nouveau_lieu.id_equip == 'Mangeoire':
                    if character.etat == 'affamé':
                        character.etat = 'repus'               
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                    else:
                        messages.error(request, f"{character.id_character} n'a pas faim!")
                        return redirect('character_detail', id_character=id_character)
                if nouveau_lieu.id_equip == 'Parc':
                    if character.etat == 'endormi':
                        character.etat = 'réveillé'               
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                    else:
                        messages.error(request, f"{character.id_character} n'a pas besoin de se défouler!")
                        return redirect('character_detail', id_character=id_character)   
                if nouveau_lieu.id_equip == 'Box':
                    if character.etat == 'repus':
                        character.etat = 'endormi'               
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                    else:
                        messages.error(request, f"{character.id_character} n'est pas repus!")
                        return redirect('character_detail', id_character=id_character)
                if nouveau_lieu.id_equip == 'Manège':
                    if character.etat == 'réveillé':
                        character.etat = 'affamé'               
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                    else:
                        messages.error(request, f"{character.id_character} n'est pas pret pour un cours!")
                        return redirect('character_detail', id_character=id_character)
                
                character.save()

                messages.success(request, f"{character.id_character} a été déplacé avec succès!")
                return redirect('character_detail', id_character=id_character)
            else:
                messages.error(request, f"Le lieu {character.lieu.id_equip} est déjà occupé. Impossible de déplacer le personnage.")
                return redirect('character_detail', id_character=id_character)
    
    else:
        form = MoveForm()
    return render(request, 'playground/character_detail.html', {
        'character': character,
        'lieu': character.lieu,
        'form': form,
    })





