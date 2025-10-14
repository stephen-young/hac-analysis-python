import hydra
from pathlib import Path
from omegaconf import DictConfig, OmegaConf


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    print(Path.cwd())

    db_index_loc = Path(cfg.paths.metadata_dir) / cfg.metadata.database
    print(db_index_loc)
    print(db_index_loc.exists())


if __name__ == "__main__":
    main()
