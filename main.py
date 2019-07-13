import argparse
from trainer import BaseTrainer, MetaTrainer
from distributed_run import distributed_main
import torch


def main(args):
    args.devices = [int(gpu) for gpu in args.devices.split('_')]
    args.use_cuda = args.use_cuda and torch.cuda.is_available()
    args.distributed = (args.use_cuda and args.multiprocessing_distributed)

    if args.distributed:
        distributed_main(args)
    else:
        if args.meta:
            trainer = MetaTrainer(args)
        else:
            trainer = BaseTrainer(args)
        trainer.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="debugging mode")
    # parser.add_argument("--meta", action="store_true", help="whether to trian meta")
    parser.add_argument("--meta", default=False, help="whether to trian meta")
    parser.add_argument("--bert_model", default="bert-base-uncased", type=str, help="bert model")
    parser.add_argument("--max_seq_length", default=384, type=int, help="max sequence length")
    parser.add_argument("--max_query_length", default=64, type=int, help="max query length")
    parser.add_argument("--doc_stride", default=128, type=int)
    parser.add_argument("--batch_size", default=64, type=int, help="batch size")
    parser.add_argument("--epochs", default=2, type=int, help="number of epochs")
    parser.add_argument("--lr", default=3e-5, type=float)
    parser.add_argument("--warmup_proportion", default=0.1, type=float)
    parser.add_argument("--gradient_accumulation_steps", default=1, type=int, help="gradient_accumulation_steps")
    parser.add_argument("--bert_config_file", default="./data/bert_base_config.json", type=str, help="bert config file")

    parser.add_argument("--do_lower_case", default=True, help="do lower case on text")
    parser.add_argument("--use_cuda", default=True, help="use cuda or not")
    parser.add_argument("--curriculum", default=False, help="enable curriculum mechanism")

    parser.add_argument("--train_folder"
                        , default="./data/train"
                        , type=str, help="path of training data file")
    parser.add_argument("--level_folder"
                        , default="./generator/difficulty"
                        , type=str, help="path of difficulty file")
    parser.add_argument("--pickled_folder"
                        , default="./pickled_data"
                        , type=str, help="path of saved pickle file")

    parser.add_argument("--devices",
                        type=str,
                        default='0_1_2_3',
                        help="gpu device ids to use")

    parser.add_argument("--workers", default=4
                        , help="Number of processes(workers) per node."
                               "It should be equal to the number of gpu devices to use in one node")
    parser.add_argument("--world_size", default=1,
                        help="Number of total workers. Initial value should be set to the number of nodes."
                             "Final value will be Num.nodes * Num.devices")
    parser.add_argument("--rank", default=0, help="The priority rank of current node.")
    parser.add_argument("--dist_backend", default="nccl",
                        help="Backend communication method. NCCL is used for DistributedDataParallel")
    parser.add_argument("--dist_url", default="tcp://127.0.0.1:9999", help="DistributedDataParallel server")
    parser.add_argument("--gpu", default=None,
                        help="Manual setting of gpu device. If it is not None, all parallel processes are disabled")
    parser.add_argument("--multiprocessing_distributed", default=True, help="Use multiprocess distribution or not")
    parser.add_argument("--save_model_by_all_devices", default=False, help="Save best model in all devices or not")
    parser.add_argument("--make_sample_prediction", default=False, help="Make sample prediction during training or not")
    parser.add_argument("--random_seed", default=2019, help="random state (seed)")

    args = parser.parse_args()

    main(args)
