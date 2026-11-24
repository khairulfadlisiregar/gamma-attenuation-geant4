#include "PrimaryGeneratorAction.hh"

#include "G4ParticleTable.hh"
#include "G4Gamma.hh"
#include "G4SystemOfUnits.hh"
#include "G4Event.hh"

PrimaryGeneratorAction::PrimaryGeneratorAction() {
  fParticleGun = new G4ParticleGun(1);

  auto* gamma = G4Gamma::GammaDefinition();
  fParticleGun->SetParticleDefinition(gamma);

  fParticleGun->SetParticleEnergy(662.0 * keV);
  fParticleGun->SetParticlePosition(G4ThreeVector(0.0, 0.0, -15.0 * cm));
  fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0.0, 0.0, 1.0));
}

PrimaryGeneratorAction::~PrimaryGeneratorAction() {
  delete fParticleGun;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent) {
  fParticleGun->GeneratePrimaryVertex(anEvent);
}
