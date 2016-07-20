void subTree(TString dir, TString cut, TString newFile){
    TTree *in  = (TTree *)gFile->Get(dir+"/fitter_tree");
    TFile *fout = new TFile(newFile, "RECREATE");
    TDirectory *dout = fout->mkdir(dir); dout->cd();

    TTree *out = in->CopyTree(cut);
    std::cout << "INPUT TREE (" << in->GetEntries() << " ENTRIES)" << std::endl;
    std::cout << "OUTPUT TREE (" << out->GetEntries() << " ENTRIES)" << std::endl;
    dout->WriteTObject(out, "fitter_tree");
    fout->Close();
}
